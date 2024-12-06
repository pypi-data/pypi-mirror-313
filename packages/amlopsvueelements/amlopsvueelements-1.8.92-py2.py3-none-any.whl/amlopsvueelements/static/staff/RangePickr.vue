<script setup lang="ts">
import { defineProps, defineModel, computed, watch, nextTick } from 'vue'
import moment from 'moment-timezone'

import { FlatPickr, SelectField } from 'shared/components'
import TimeAutoComplete from '@/components/common/TimeAutoComplete.vue'

interface Props {
  maxDiff: number // in hours
  timezoneOptions?: { id: number | string, label: string; value: string }[]
  calendarTimezone?: string
  isLoadingTimezoneOptions?: boolean
  alldayMandatory?: boolean
  readonly?: boolean
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  maxDiff: 0,
  alldayMandatory: false,
  readonly: false,
  disabled: false
})
const model = defineModel<Date[] | string[]>('range')
const timezone = defineModel<string >('timezone')
const allDay = defineModel<boolean>('allDay')

const updateModelValue = (
  [nStartDate,
  nStartTime,
  nEndDate,
  nEndTime]: string[]
) => {
  const tzTmp = timezone.value === 'local'? moment.tz.guess(): timezone.value ?? 'UTC'

  // Convert the times depending on the modal' timezone to UTC
  const [ startDateTime, endDateTime ] = 
    [ nStartDate + 'T' +  nStartTime, nEndDate + 'T' + nEndTime ]
    .map(date => 
        moment.tz(date, 'YYYY-MM-DD HH:mm', tzTmp)
        .tz('UTC').format('YYYY-MM-DD HH:mm')
      )
      
  model.value = [startDateTime, endDateTime]
}

// Automatically adjust the endDate & endTime to maintain the time difference with the startDate & startTime.
const getAdjustedEndDatetime = (
  [newStartDate, newStartTime]: string[],
  [oldStartDate, oldStartTime]: string[]
): string[] => {
  if (allDay.value) {
    return [newStartDate, endTime.value]
  } else {
    const endDatetime = moment(endDate.value, 'YYYY-MM-DD').add(moment.duration(endTime.value)),
      oldStartDatetime = moment(oldStartDate, 'YYYY-MM-DD').add(moment.duration(oldStartTime)),
      diff = moment.duration(endDatetime.diff(oldStartDatetime)),
      newEndDatetime = moment(newStartDate, 'YYYY-MM-DD')
        .add(moment.duration(newStartTime))
        .add(diff)

    if (diff.asHours() <= 0) {
      if (diff.asHours() < -props.maxDiff) {
        const newStartDateTime = moment(newStartDate, 'YYYY-MM-DD').add(
            moment.duration(newStartTime)
          ),
          newEndDatetime = moment(newStartDateTime).add(props.maxDiff, 'hours')
        return [newEndDatetime.format('YYYY-MM-DD'), newEndDatetime.format('HH:mm')]
      }
      return [endDate.value, endTime.value]
    } else {
      return [newEndDatetime.format('YYYY-MM-DD'), newEndDatetime.format('HH:mm')]
    }
  }
}

const startDate = computed<string>({
  get() {
      return moment
        .tz(model.value?.[0], 'UTC')
        .tz(timezone.value === 'local'? moment.tz.guess(): timezone.value ?? 'UTC')
        .format('YYYY-MM-DD')
      },
  set(newValue) {
    if(moment(newValue).isSame(startDate.value)) {
      return
    }
    const [newEndDate, newEndTime] = getAdjustedEndDatetime(
      [newValue, startTime.value],
      [startDate.value, startTime.value]
      )
    updateModelValue([newValue, startTime.value, newEndDate, newEndTime])
  }
})
const startTime = computed<string>({
  get() {
    return moment
      .tz(model.value?.[0], 'UTC')
      .tz(timezone.value === 'local'? moment.tz.guess(): timezone.value ?? 'UTC')
      .format('HH:mm')
  },
  set(newValue) {    
    if(moment(newValue, 'HH:mm').isSame(moment(startTime.value, 'HH:mm'))) {
      return
    }
    const [newEndDate, newEndTime] = getAdjustedEndDatetime(
      [startDate.value, newValue],
      [startDate.value, startTime.value]
      )
      updateModelValue([startDate.value, newValue, newEndDate, newEndTime])
  }
})
const endDate = computed<string>({
  get() {
    return moment
      .tz(model.value?.[1], 'UTC')
      .tz(timezone.value === 'local'? moment.tz.guess(): timezone.value ?? 'UTC')
      .format('YYYY-MM-DD')
  },
  set(newValue) {
    if(moment(newValue).isSame(endDate.value)) {
      return
    }
    updateModelValue([startDate.value, startTime.value, newValue, endTime.value])
  }
})
const endTime = computed<string>({
  get() {
    return moment
      .tz(model.value?.[1], 'UTC')
      .tz(timezone.value === 'local'? moment.tz.guess(): timezone.value ?? 'UTC')
      .format('HH:mm')
  },
  set(newValue) {
    if(moment(newValue, 'HH:mm').isSame(moment(endTime.value, 'HH:mm'))) {
      return
    }
    updateModelValue(
      [startDate.value,
      startTime.value,
      moment(endDate.value).isSame(moment(startDate.value)) &&
        moment(newValue, 'HH:mm').isBetween(
          moment('00:00', 'HH:mm'),
          moment(startTime.value, 'HH:mm'),
          undefined,
          '[)'
        )
        ? moment(endDate.value).add(1, 'day').format('YYYY-MM-DD') // When selecting a time for the next date, update the endDate accordingly.
        : endDate.value,
      newValue]
    )
  }
})

const startDatetimeUTC = computed(() => {
    return moment
      .tz(model.value?.[0], 'UTC')
      .format('YYYY-MM-DD HH:mm')
  })
const endDatetimeUTC = computed(
  () => {
    return moment
      .tz(model.value?.[1], 'UTC')
      .format('YYYY-MM-DD HH:mm')
  })
watch(
  () => [allDay.value, props.alldayMandatory],
  async () => {
    if(props.alldayMandatory){
      allDay.value = true
    } else if (allDay.value && moment(startDate.value).isSame(endDate.value)) {
      startTime.value = moment(startDate.value).startOf('date').format('HH:mm')
      await nextTick()
      endDate.value = moment(startDate.value).format('YYYY-MM-DD')
      await nextTick()
      endTime.value = moment(startDate.value).endOf('date').format('HH:mm')
    }
  }
)
</script>

<template>
  <div class="mb-[1rem]">
    <div class="flex align-items-center gap-x-2">
      <div class="flex border rounded-[8px] date-time-picker overflow-hidden">
        <FlatPickr
          :config="{
            allowInput: true,
            altInput: true,
            altFormat: 'Y-m-d',
            locale: { firstDayOfWeek: 1 }
          }"
          class="flex-[2]"
          v-model="startDate"
          placeholder=""
          :disabled="disabled"
        />
        <TimeAutoComplete v-model="startTime" class="flex-1" v-if="!allDay" />
      </div>
      <span> - </span>
      <div class="flex border rounded-[8px] date-time-picker overflow-hidden">
        <TimeAutoComplete
          v-model="endTime"
          :from="moment(endDate).isSame(moment(startDate)) ? startTime : undefined"
          :max-time="
            moment(endDate).isSame(moment(startDate))
              ? undefined
              : moment(startDate).add(moment.duration(startTime)).add(1, 'day').format('HH:mm')
          "
          class="flex-1"
          v-if="!allDay"
        />
        <FlatPickr
          :config="{
            allowInput: true,
            altInput: true,
            altFormat: 'Y-m-d',
            locale: { firstDayOfWeek: 1 }
          }"
          class="flex-[2]"
          v-if="allDay || startDate !== endDate"
          v-model="endDate"
          placeholder=""
        />
      </div>
    </div>
    <small class="text-body-secondary form-text italic">
      ({{ startDatetimeUTC }} UTC) - ({{ endDatetimeUTC }} UTC)
    </small>
  </div>
  <div class="mb-[1rem] flex gap-x-2 align-items-center">
    <div class="form-check w-[100px]">
      <input
        v-model="allDay"
        :checked="allDay"
        :disabled="alldayMandatory"
        :readonly="alldayMandatory"
        class="form-check-input"
        type="checkbox"
        id="all-day-check"
      />
      <label class="form-check-label !mb-0" for="all-day-check"> All day </label>
    </div>
    <SelectField
      :options="timezoneOptions"
      :reduce="(option: any) => option.value"
      label="label"
      :loading="isLoadingTimezoneOptions"
      v-model="timezone"
      :clearable="false"
      :append-to-body="false"
      placeholder=""
      class="mb-0 flex-1"
    />
  </div>
</template>

<style scoped lang="scss">
:deep(input.leg-date-picker) {
  height: 2.5rem !important;
  padding: 5px 1rem !important;
  border: none !important;
  border-radius: unset !important;
  outline: unset;
  ::placeholder {
    text-align: center;
  }

  &:focus {
    box-shadow: unset;
    background-color: #88888838;
  }
  &:hover {
    background-color: #88888838;
  }
}
.date-time-picker:hover {
  box-shadow:
    0 1px 2px 0 rgba(0, 0, 0, 0.07),
    0 0 0 0.18rem rgba(81, 93, 138, 0.25);
}
</style>
