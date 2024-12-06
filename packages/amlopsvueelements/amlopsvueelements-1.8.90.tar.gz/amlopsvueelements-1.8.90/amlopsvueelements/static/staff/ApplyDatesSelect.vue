<script setup lang="ts">
import { computed } from 'vue'
import moment from 'moment-timezone'
import { Dropdown } from 'floating-vue'
import { BButton } from 'bootstrap-vue-next'

import { InputField } from 'shared/components'
import 'floating-vue/dist/style.css'

interface Props {
  modelValue: number[] | undefined
  placeholder?: string
  disabled?: boolean
  start_date?: string | undefined
  end_date?: string | null
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Select Dates',
  disabled: false
})
const emit = defineEmits(['update:modelValue'])

const dates = computed<number[]>(() => {
  const ret = []
  for (let i = 1; i <= 31; i++) {
    ret.push(i)
  }

  return ret
})
const description = computed<string>(() => {
  return props.modelValue?.join(', ') ?? ''
})

const handleDateClick = (date: number) => {
  if (!props.modelValue || !props.modelValue.length) {
    emit('update:modelValue', [date])
    return
  }

  let newValue: number[]
  const index = props.modelValue.indexOf(date)
  if (index > -1) {
    newValue = [...props.modelValue.slice(0, index), ...props.modelValue.slice(index + 1)]
  } else {
    let i
    for (i = 0; i < props.modelValue.length; i++) {
      if (props.modelValue[i] > date) {
        break
      }
    }
    newValue = [...props.modelValue.slice(0, i), date, ...props.modelValue.slice(i)]
  }

  emit('update:modelValue', newValue)
}

const handleClear = () => {
  emit('update:modelValue', [])
}

const handleSelectAll = () => {
  emit('update:modelValue', dates.value)
}

const handleSelectAvailable = () => {
  if (!props.start_date || !props.end_date) {
    return
  }

  const days: number[] = []
  for (
    const iDate = moment(props.start_date);
    iDate.isSameOrBefore(props.end_date);
    iDate.add(1, 'day')
  ) {
    if (days.length === 31) {
      break
    }

    const date = iDate.get('date')
    if (days.includes(date)) {
      continue
    }
    days.push(date)
  }
  days.sort((a, b) => a - b)
  emit('update:modelValue', days)
}
</script>

<template>
  <Dropdown placement="bottom-start" :disabled="disabled">
    <InputField
      :model-value="description"
      :disabled="disabled"
      :placeholder="placeholder"
      readonly
      class="mb-0"
    />
    <template #popper>
      <div class="actions-container">
        <BButton size="sm" variant="outline-danger" class="mr-1" @click="handleClear">
          Clear
        </BButton>
        <BButton size="sm" variant="outline-primary" class="mr-1" @click="handleSelectAll">
          Select All
        </BButton>
        <BButton size="sm" variant="outline-primary" @click="handleSelectAvailable">
          Select Available
        </BButton>
      </div>
      <div class="days" tabindex="-1">
        <div class="days-panel">
          <span
            v-for="date of dates"
            :key="date"
            class="day"
            :class="{ selected: modelValue?.includes(date) }"
            tabindex="-1"
            @click="() => handleDateClick(date)"
          >
            {{ date }}
          </span>
        </div>
      </div>
    </template>
  </Dropdown>
</template>

<style scoped lang="scss">
.actions-container,
.days {
  @apply p-[12px];
}
.actions-container {
  border-bottom: 0.0625rem solid #e5e7eb;
}
.days {
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}
.days-panel {
  width: 273px;
  padding: 0;
  outline: 0;
  text-align: center;
  box-sizing: border-box;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  transform: translate3d(0px, 0px, 0px);
  opacity: 1;
}
.day {
  background: 0 0;
  border: 1px solid transparent;
  border-radius: 150px;
  box-sizing: border-box;
  color: #484848;
  cursor: pointer;
  font-weight: 400;
  width: 39px;
  height: 39px;
  line-height: 39px;
  margin: 0;
  display: inline-block;
  position: relative;
  justify-content: center;
  text-align: center;

  &:hover {
    cursor: pointer;
    outline: 0;
    background: #e2e2e2;
    border-color: #e2e2e2;
  }
  &.selected {
    background: #515d8a;
    box-shadow: none;
    color: #fff;
    border-color: #515d8a;
  }
}
</style>
