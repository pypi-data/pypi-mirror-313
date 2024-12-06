<script setup lang="ts">
import { defineModel, defineEmits, ref, computed, watchEffect } from 'vue'
import { watchDebounced } from '@vueuse/core'
import moment, { type Moment } from 'moment-timezone'

import { getFlooredTime } from '@/utils/date'

import { Dropdown } from 'floating-vue'
import { InputField } from 'shared/components'
import 'floating-vue/dist/style.css'

const OPTION_HEIGHT = 42

const _getHumanizedDiff = (a: Moment, b: Moment): string => {
  const diff = moment.duration(b.diff(a))
  const hours = diff.asHours()
  if (hours < 1) {
    return `${diff.asMinutes()} mins`
  } else {
    return `${hours} hr${hours === 1 ? '' : 's'}`
  }
}

export interface Option {
  label: string
  value: string
}

interface Props {
  from?: string
  maxTime?: string
  placeholder?: string
  disabled?: boolean
  class?: string
}

const model = defineModel<string>()
const emits = defineEmits(['blur'])
const props = withDefaults(defineProps<Props>(), {
  placeholder: '',
  disabled: false
})

const className = props.class

const shownDropdown = ref<boolean>(false)
const inputValue = ref()
const listElement = ref()

const options = computed<Option[]>(() => {
  const ret = []

  const iStartDate = props.from
      ? moment().startOf('day').add(moment.duration(props.from))
      : moment().startOf('day'),
    iEndDate = props.from ? moment(iStartDate).add(1, 'hour') : moment(iStartDate).add(1, 'day')
  let iDate: Moment
  for (iDate = moment(iStartDate); iDate.isBefore(iEndDate); iDate.add(15, 'minutes')) {
    ret.push({
      label:
        iDate.format('HH:mm') + (props.from ? ` (${_getHumanizedDiff(iStartDate, iDate)})` : ''),
      value: iDate.format('HH:mm')
    })
  }

  if (!props.from) {
    return ret
  }

  iEndDate.add(23, 'hours')
  for (; iDate.isBefore(iEndDate); iDate.add(30, 'minutes')) {
    ret.push({
      label:
        iDate.format('HH:mm') + (props.from ? ` (${_getHumanizedDiff(iStartDate, iDate)})` : ''),
      value: iDate.format('HH:mm')
    })
  }

  return ret
})

const onOptionClick = (value: string) => {
  model.value = inputValue.value = value
}

const onFocus = () => {
  shownDropdown.value = true
}

const onBlur = () => {
  emits('blur')

  // use setTimeout to ensure that the dropdown remains open until the click event on the options is detected.
  setTimeout(() => {
    const inputTime = moment(inputValue.value, 'HH:mm')
    if (inputTime.isValid()) {
      if (props.maxTime && inputTime.isSameOrAfter(moment(props.maxTime, 'HH:mm'))) {
        model.value = inputValue.value = moment(props.maxTime, 'HH:mm')
          .subtract(1, 'minutes')
          .format('HH:mm')
      } else {
        model.value = inputValue.value = inputTime.format('HH:mm')
      }
    } else {
      inputValue.value = model.value
    }

    shownDropdown.value = false
  }, 200)
}

const onKeydown = (event: KeyboardEvent) => {
  switch (event.code) {
    case 'ArrowUp':
    case 'ArrowDown': {
      event.preventDefault()

      const inputTime = moment(inputValue.value, 'HH:mm')
      if (!inputTime.isValid()) {
        return
      }

      const from = props.from ? moment(props.from, 'HH:mm') : moment().startOf('day'),
        diff = moment.duration(inputTime.diff(from)),
        offset = props.from
          ? moment
              .duration(from.diff(getFlooredTime(props.from, diff.asHours() > 1 ? 30 : 15)))
              .asMinutes()
          : 0,
        nearestTime = getFlooredTime(
          moment(inputTime).subtract(offset, 'minutes'),
          props.from && diff.asHours() > 1 ? 30 : 15
        ).add(offset, 'minutes')

      model.value = inputValue.value =
        event.code === 'ArrowUp' && moment.duration(inputTime.diff(nearestTime)).asMinutes() > 0
          ? nearestTime.format('HH:mm')
          : nearestTime
              .add(
                (props.from && diff.asHours() >= 1 ? 30 : 15) * (event.code === 'ArrowUp' ? -1 : 1),
                'minutes'
              )
              .format('HH:mm')
      break
    }
    default:
  }
}

watchEffect(() => {
  inputValue.value = model.value
})

// Automatic scrolling to the nearest time option.
watchDebounced(
  [listElement, shownDropdown, inputValue],
  () => {
    if (!shownDropdown.value || !listElement.value) {
      return
    }

    const inputTime = moment(inputValue.value, 'HH:mm')
    if (!inputTime.isValid()) {
      return
    }

    const from = props.from ? moment(props.from, 'HH:mm') : moment().startOf('day'),
      diff = moment.duration(inputTime.diff(from)),
      offset = props.from
        ? moment
            .duration(from.diff(getFlooredTime(props.from, diff.asHours() > 1 ? 30 : 15)))
            .asMinutes()
        : 0,
      nearestTime = getFlooredTime(
        moment(inputTime).subtract(offset, 'minutes'),
        props.from && diff.asHours() > 1 ? 30 : 15
      ).add(offset, 'minutes'),
      diffWithNearest = moment.duration(nearestTime.diff(from))

    const targetScrollPosition =
      props.from && diffWithNearest.asHours() > 1
        ? Math.floor(diffWithNearest.asMinutes() / 30) * OPTION_HEIGHT // (Math.floor(diffWithNearest.asMinutes() / 30) + 2 - 2) * OPTION_HEIGHT
        : (Math.floor(diffWithNearest.asMinutes() / 15) - 2) * OPTION_HEIGHT

    listElement.value.scrollTo(0, targetScrollPosition)
  },
  { debounce: 50, maxWait: 1000 }
)
</script>

<template>
  <Dropdown
    placement="bottom-start"
    :disabled="disabled"
    :triggers="[]"
    :shown="shownDropdown"
    :auto-hide="false"
    :class="className"
  >
    <InputField
      v-bind="$attrs"
      v-model="inputValue"
      :disabled="disabled"
      :placeholder="placeholder"
      @focus="onFocus"
      @blur="onBlur"
      @keydown="onKeydown"
      class="mb-0 border-none"
    />
    <template #popper>
      <div class="min-w-[180px] h-[210px] overflow-y-auto" ref="listElement">
        <div class="list-group list-group-flush">
          <div
            v-for="option of options"
            :key="option.value"
            @click="onOptionClick(option.value)"
            class="list-group-item list-group-item-action h-[42px] !flex align-items-center"
            :class="{
              active: inputValue === option.value,
              disabled: maxTime
                ? moment(option.value, 'HH:mm').isSameOrAfter(moment(maxTime, 'HH:mm'))
                : false
            }"
          >
            <div>{{ option.label }}</div>
          </div>
        </div>
      </div>
    </template>
  </Dropdown>
</template>

<style scoped lang="scss">
:deep(.u-input-wrapper) {
  height: 2.5rem !important;
  border: none !important;
  border-radius: unset !important;
  outline: unset;
  box-shadow: unset !important;

  padding: 0;
  & > input {
    width: 100%;
    height: 100%;
    padding: 5px 0.5rem !important;
    &:hover {
      background-color: #88888838 !important;
    }
    &:focus {
      box-shadow: unset;
      background-color: #88888838 !important;
    }
  }
}
</style>
