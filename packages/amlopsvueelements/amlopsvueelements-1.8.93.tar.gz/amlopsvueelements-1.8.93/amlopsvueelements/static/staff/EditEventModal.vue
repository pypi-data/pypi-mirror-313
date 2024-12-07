<script setup lang="ts">
import { computed, nextTick, reactive, ref, watch, watchEffect } from 'vue'
// @ts-ignore
import { useVuelidate } from '@vuelidate/core'
import { required, requiredIf, helpers } from '@vuelidate/validators'
import type { DateSelectArg } from '@fullcalendar/core'
import type { AxiosError } from 'axios'
import moment, { tz } from 'moment-timezone'
import { useMutation } from '@tanstack/vue-query'
import { getFlooredTime, isAllDay } from '@/utils/date'

import {
  BAlert,
  BButton,
  BForm,
  BFormGroup,
  BFormInvalidFeedback,
  BFormTextarea,
  BModal,
  BRow,
  BCol
} from 'bootstrap-vue-next'
import { FlatPickr, SelectField } from 'shared/components'
import ApplyDatesSelect from '@/components/common/ApplyDatesSelect.vue'
import RangePickr from '@/components/calendar/RangePickr.vue'

import type { EventApi } from '@fullcalendar/core'
import type { Person } from '@/models/Person'
import type {
  SpecificEntryPayload,
  SpecificEntryPersonPopulated,
  BlanketEntryPersonPopulated,
  BlanketEntryPayload
} from '@/models/Entry'
import type { EntryType } from '@/models/EntryType'
import { setLabelSuffix, useTimezones } from '@/composables/useTimezones'
import { usePeople } from '@/composables/usePeople'
import { useEntryTypes } from '@/composables/useEntryTypes'

import entryService from '@/services/EntryService'

import ApplyDaysSelect from '@/components/common/ApplyDaysSelect.vue'
import ApplyWeeksSelect from '@/components/common/ApplyWeeksSelect.vue'
import ConfirmModal, { type ConfirmOption } from '@/components/calendar/ConfirmModal.vue'
import type { Timezone } from '@/models/Timezone'

export type EventEditMode = 'add' | 'quick-add-sickness-absence' | 'edit'

type RepeatFreq = 'no-repeat' | 'daily' | 'weekly'
interface RepeatFreqOption {
  label: string
  value: RepeatFreq
}

interface Props {
  mode: EventEditMode
  event?: EventApi
  selectionInfo?: DateSelectArg
  calendarRef?: any
  calendarTimezone: {
    label: string,
    value: string
  }
}

interface FormValues {
  id: number | undefined
  person: Person | undefined
  entry_type: EntryType | undefined
  range: string[] | undefined
  allDay: boolean | undefined
  timezone: string | number
  repeatFreq: RepeatFreq
  until: string | null
  applied_on_dates: number[] | undefined
  applied_on_days: number[] | undefined
  applied_on_weeks: number[] | undefined
  comment: string | undefined
  replaces_other_entry: number | null | undefined
  replaces_own_entry: number | null | undefined
  excluded_dates: string[]
}

const defaultValues: FormValues = {
  id: undefined,
  person: undefined,
  entry_type: undefined,
  range: [],
  allDay: false,
  timezone: 1, // TODO: Remove it (Bind directly to the person's timezone)
  repeatFreq: 'no-repeat',
  until: null,
  applied_on_dates: undefined,
  applied_on_days: undefined,
  applied_on_weeks: [0],
  comment: undefined,
  replaces_other_entry: undefined,
  replaces_own_entry: undefined,
  excluded_dates: []
}

const open = defineModel<boolean>('open')
const props = withDefaults(defineProps<Props>(), {
  mode: 'add'
})
const emit = defineEmits(['event-created', 'hide'])

const { data: tzData, isLoading: isLoadingTimezones } = useTimezones()
const { data: people, isLoading: isLoadingPeople } = usePeople()
const { data: entryTypes, isLoading: isLoadingEntryTypes } = useEntryTypes()

const isDelete = ref<boolean>(false)
const isConfirmModalOpen = ref<boolean>(false)
const modeRef = ref<EventEditMode>(props.mode)
const twoMutateMode = ref<boolean>(false)
const untilState = ref<'never' | 'on'>('never')
const weeklyFollowing = ref<boolean>(false)
const timezones = ref<Timezone[]>()
const startOfModal = ref<string>()

const repeatFreqOptions = computed<RepeatFreqOption[]>(() => [
  {
    label: "Doesn't repeat",
    value: 'no-repeat'
  },
  {
    label: 'Daily',
    value: 'daily'
  },
  {
    label: 'Weekly',
    value: 'weekly'
  }
])
const isBlanketEntry = computed(() => {
  return props.event?.id.startsWith('blanket') ?? false
})
const entry = computed<SpecificEntryPersonPopulated | BlanketEntryPersonPopulated>(
  () => props.event?.extendedProps as SpecificEntryPersonPopulated | BlanketEntryPersonPopulated
)
const selectedDate = computed<string>(() => moment.utc(props.event?.start).format('YYYY-MM-DD'))

const { isPending, mutate } = useMutation({
  mutationFn: ({
    entries,
    isDelete
  }: {
    entries: SpecificEntryPayload[] | BlanketEntryPayload[]
    isDelete?: boolean
  }) =>
    twoMutateMode.value
      ? entryService.updateBlanketEntries(genPayloadBased()).then(() => {
          entryService.createSpecificEntries(entries)
        })
      : values.repeatFreq === 'weekly'
        ? weeklyFollowing.value
          ? isDelete
            ? entryService
                .deleteBlanketEntries(entries)
                .then(() =>
                  entryService.createBlanketEntries(
                    genPayloadBased(
                      false,
                      moment(selectedDate.value).subtract(1, 'day').format('YYYY-MM-DD'),
                      selectAppliedOnWeeks('following', true)
                    )
                  )
                )
            : entryService
                .updateBlanketEntries(
                  genPayloadBased(
                    false,
                    moment(selectedDate.value).subtract(1, 'day').format('YYYY-MM-DD'),
                    selectAppliedOnWeeks('following')
                  )
                )
                .then(() => entryService.createBlanketEntries(entries))
          : isDelete
            ? entryService.deleteBlanketEntries(entries)
            : modeRef.value === 'edit'
              ? entryService.updateBlanketEntries(entries)
              : entryService.createBlanketEntries(entries)
        : isDelete
          ? entryService.deleteSpecificEntries(entries)
          : modeRef.value === 'edit'
            ? entryService.updateSpecificEntries(entries)
            : entryService.createSpecificEntries(entries),
  onSuccess: (data) => {
    emit('event-created', data)
    open.value = false
  },
  onError: (error: AxiosError) => {
    if (!error.response) {
      non_field_errors.value = ['Network error']
      return
    }

    const errors = (error.response.data as any).errors
      ? (error.response.data as any).errors[0]
      : undefined
    if (!errors) {
      non_field_errors.value = ['Unknown error']
    } else if (errors.non_field_errors) {
      non_field_errors.value = errors.non_field_errors
    } else if (errors.message) {
      non_field_errors.value = [errors.message]
    } else {
      $externalResults.value = errors
    }
  }
})

const non_field_errors = ref<string[]>([])
const $externalResults = ref({})

const rules = computed(() => ({
  id: {},
  person: { required },
  entry_type: { required },
  range: {
    required,
    lessInvalid: helpers.withMessage(
      () => 'The event must end after its start',
      (range: Date[] | string[]) => {
        if (!range || range.length !== 2) {
          return true
        }

        return values.allDay
          ? moment(range[0]).isSameOrBefore(moment(range[1]))
          : moment(range[0]).isBefore(moment(range[1]))
      }
    ),
    overInvalid: helpers.withMessage(
      () => 'The event duration must not exceed 24 hours',
      (range: Date[] | string[]) => {
        if (!range || range.length !== 2) {
          return true
        }

        return moment.duration(moment(range[1]).diff(range[0])).asHours() < 24
      }
    )
  },
  timezone: {},
  repeatFreq: { required },
  until: { requiredIf: requiredIf(values.repeatFreq !== 'no-repeat' && untilState.value === 'on') },
  applied_on_dates: { requiredUnless: requiredIf(values.repeatFreq === 'daily') },
  applied_on_days: { requiredIf: requiredIf(values.repeatFreq === 'weekly') },
  applied_on_weeks: { requiredIf: requiredIf(values.repeatFreq === 'weekly') },
  comment: { requiredIf: requiredIf(values.entry_type?.requires_comment ?? false) },
  replaces_other_entry: {},
  replaces_own_entry: {}
}))
const timezoneValue = computed<string>({
  get() {
    return timezones.value?.filter(tz => 
      values.timezone === (tz.id)
      )[0]?.value ?? 'UTC'
  },
  set(newValue) {
    values.timezone = timezones.value?.filter(tz => 
      tz.value === (newValue)
    )[0].id ?? 'UTC'
  }
})

const values = reactive<FormValues>({
  id: defaultValues.id,
  person: defaultValues.person,
  entry_type: defaultValues.entry_type,
  range: defaultValues.range,
  allDay: defaultValues.allDay,
  timezone: defaultValues.timezone, // not string, number to indicate the timezone ID
  repeatFreq: defaultValues.repeatFreq,
  until: defaultValues.until,
  applied_on_dates: defaultValues.applied_on_dates,
  applied_on_days: defaultValues.applied_on_days,
  applied_on_weeks: defaultValues.applied_on_weeks,
  comment: defaultValues.comment,
  replaces_other_entry: defaultValues.replaces_other_entry,
  replaces_own_entry: defaultValues.replaces_own_entry,
  excluded_dates: defaultValues.excluded_dates
})
const v$ = useVuelidate(rules, values, { $externalResults, $autoDirty: true })

const selectAppliedOnWeeks = (action: ConfirmOption, isReverseFollowing = false) => {
  // The week number starting from start_date of event
  let weekno = 0
  for (
    const iDate = moment(values.range?.[0]).startOf('week');
    iDate.isSameOrBefore(props.event?.start);
    iDate.add(1, 'week')
  ) {
    weekno++
  }
  let weeks: number[]
  if (action === 'only') {
    weeks = [weekno] // no need anymore
  } else if (action === 'following') {
    if (!isReverseFollowing) {
      const index = values?.applied_on_weeks?.indexOf(weekno)
      weeks =
        !values.applied_on_weeks?.length || values.applied_on_weeks[0] === 0
          ? [0]
          : values.applied_on_weeks!.slice(index)
    } else {
      const index = values?.applied_on_weeks?.indexOf(weekno) ?? 0
      weeks =
        !values.applied_on_weeks?.length || values.applied_on_weeks[0] === 0
          ? [0]
          : values.applied_on_weeks!.slice(0, index + 1)
    }
  } else {
    weeks = values.applied_on_weeks ?? []
  }
  return weeks
}

const selectAppliedOnDates = (action?: ConfirmOption) => {
  const calendarTZ = props.calendarTimezone.value === 'local'? moment.tz.guess(): props.calendarTimezone.value
  const date = moment.tz(props.event?.start, calendarTZ).tz('UTC').get('date')

  let dates: number[]
  if (action === 'only') {
    dates = [date]
  } else if (action === 'following') {
    const index = values.applied_on_dates?.indexOf(date)
    dates = values.applied_on_dates?.slice(index) ?? []
  } else {
    dates = values.applied_on_dates ?? []
  }

  return dates
}

const onConfirm = (action: ConfirmOption) => {
  const calendarTZ = props.calendarTimezone.value === 'local'? moment.tz.guess(): props.calendarTimezone.value

  const entryPayload: SpecificEntryPayload | BlanketEntryPayload = {
    id: values.id,
    person: values.person?.person_id,
    team: values.person?.aml_team_id,
    start_hour: moment(values.range?.[0], 'YYYY-MM-DD HH:mm:ss').format('HH:mm:ss'),
    end_hour: moment(values.range?.[1], 'YYYY-MM-DD HH:mm:ss').format('HH:mm:ss'),
    comment: values.comment,
    start_date: moment(values.range?.[0], 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD'),
    end_date:
      values.repeatFreq === 'no-repeat'
        ? moment(values.range?.[0], 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD')
        : values.until,
    entry_type: values.entry_type?.id,
    ...(values.repeatFreq === 'weekly'
      ? {
          applied_on_days: values.applied_on_days,
          applied_on_weeks: values.applied_on_weeks
        }
      : {
          applied_on_dates: values.applied_on_dates
        }),
    ...(isBlanketEntry.value && !twoMutateMode.value
      ? { excluded_dates: values.excluded_dates }
      : {}),
    timezone: values.timezone
  }

  // Edit
  if (modeRef.value === 'edit') {
    entryPayload.flagged_for_edit = entry.value?.flagged_for_edit
    entryPayload.flagged_for_delete = entry.value?.flagged_for_delete
    if (isDelete.value) {
      entryPayload.flagged_for_delete = true
    } else {
      entryPayload.flagged_for_edit = true
    }

    if (values.repeatFreq === 'weekly') {
      entryPayload.start_date = entry.value.start_date
      if ('applied_on_weeks' in entryPayload) {
        entryPayload.applied_on_weeks = selectAppliedOnWeeks(action)
      }

      if (action === 'only') {
        if ('excluded_dates' in entryPayload) {
          if (isDelete.value) {
            const formattedDate = moment.tz(props.event!.startStr, 'YYYY-MM-DD HH:mm:ss', calendarTZ).tz('UTC')
              .format('YYYY-MM-DD')
            entryPayload?.excluded_dates?.push(formattedDate)
            entryPayload.flagged_for_edit = true
            entryPayload.flagged_for_delete = false
            if ('applied_on_weeks' in entryPayload && 'applied_on_weeks' in entry.value) {
              entryPayload.applied_on_weeks = entry.value.applied_on_weeks
            }
            isDelete.value = false
          } else {
            const startDate =
              moment.tz(props.event!.startStr, 'YYYY-MM-DD HH:mm:ss', calendarTZ).tz('UTC')
                .format('YYYY-MM-DD ') + moment(values.range?.[0]).format('HH:mm:ss')
            const endDate =
              moment.tz(props.event!.endStr, 'YYYY-MM-DD HH:mm:ss', calendarTZ).tz('UTC')
                .format('YYYY-MM-DD ') + moment(values.range?.[1]).format('HH:mm:ss')
            modeRef.value = 'add'
            values.repeatFreq = 'no-repeat'
            values.range = [startDate, endDate]
            twoMutateMode.value = true
            onConfirm('only')
            return
          }
        }
      } else if (action === 'following') {
        weeklyFollowing.value = true
        if (!isDelete.value) {
          entryPayload.start_date = moment.utc(props.event?.start).format('YYYY-MM-DD')
        }
      }
    } else {
      if ('applied_on_dates' in entryPayload) {
        entryPayload.applied_on_dates = selectAppliedOnDates(action)
      }
    }
  }
  // Add
  else {
    if (values.repeatFreq === 'daily') {
      if (values.applied_on_dates?.length) {
        if ('applied_on_dates' in entryPayload) {
          entryPayload.applied_on_dates = values.applied_on_dates
        }
      } else {
        const availableDates: number[] = []
        for (
          const iDate = moment(values.range?.[0]);
          iDate.isSameOrBefore(values.until);
          iDate.add(1, 'day')
        ) {
          if (availableDates.length === 31) {
            break
          }

          const date = iDate.get('date')
          if (availableDates.includes(date)) {
            continue
          }
          availableDates.push(date)
        }
        availableDates.sort((a, b) => a - b)
        if ('applied_on_dates' in entryPayload) {
          entryPayload.applied_on_dates = availableDates
        }
      }
    } else if (values.repeatFreq === 'no-repeat') {
      if ('applied_on_dates' in entryPayload) {
        entryPayload.applied_on_dates = [moment(values.range?.[0]).get('date')]
      }
    }
  }
  mutate({ entries: [entryPayload], isDelete: isDelete.value })
}

const genPayloadBased = (isExcludedPayload = true, tmpDate?: string | null, weeks?: number[]) => {
  const calendarTZ = props.calendarTimezone.value === 'local'? moment.tz.guess(): props.calendarTimezone.value
  
  const payload: BlanketEntryPayload = {
    id: entry.value.id,
    person: entry.value.person?.person_id,
    team: entry.value.person?.aml_team_id,
    start_hour: entry.value.start_hour,
    end_hour: entry.value.end_hour,
    comment: entry.value.comment,
    start_date: moment(entry.value.start_date).format('YYYY-MM-DD'),
    end_date: entry.value.end_date? moment(entry.value.end_date).format('YYYY-MM-DD'): null,
    entry_type: entry.value.entry_type?.id,
    applied_on_weeks: [],
    excluded_dates: [],
    timezone: entry.value.timezone.id
  }

  if ('applied_on_weeks' in entry.value && 'applied_on_days' in entry.value) {
    payload.applied_on_weeks = isExcludedPayload ? entry.value.applied_on_weeks : weeks
    payload.applied_on_days = entry.value.applied_on_days
  }

  const formattedDate = moment.tz(props.event!.startStr, 'YYYY-MM-DD HH:mm', calendarTZ)
    .tz('UTC')
    .format('YYYY-MM-DD')
  if ('excluded_dates' in entry.value) {
    payload.excluded_dates = entry.value?.excluded_dates
  }
  isExcludedPayload && payload.excluded_dates?.push(formattedDate)
  !isExcludedPayload && (payload.end_date = tmpDate)
  payload.flagged_for_delete = false
  payload.flagged_for_edit = true

  return [payload]
}

const onSubmit = async () => {
  const isValid = await v$?.value?.$validate()
  non_field_errors.value = []

  if (!isValid) {
    return
  }

  isDelete.value = false
  if (modeRef.value === 'edit') {
    if (values.repeatFreq === 'no-repeat') {
      onConfirm('all')
    } else {
      isConfirmModalOpen.value = true
    }
  } else {
    onConfirm('all')
  }
}

const onCancel = () => {
  open.value = false
}

const onDelete = () => {
  isDelete.value = true
  if (values.repeatFreq === 'no-repeat') {
    onConfirm('all')
  } else {
    isConfirmModalOpen.value = true
  }
}

const resetForm = async () => {
  const calendarTZ = props.calendarTimezone.value === 'local'? moment.tz.guess(): props.calendarTimezone.value

  if (twoMutateMode.value) twoMutateMode.value = false
  if (weeklyFollowing.value) weeklyFollowing.value = false
  if (modeRef.value === 'edit') {
      untilState.value = entry.value.end_date ? 'on' : 'never'
    }

  // Edit
  if (entry.value) {
    values.id = entry.value.id
    values.person = entry.value.person
    values.entry_type = entry.value.entry_type
    if(isBlanketEntry.value) {
      values.range = [
        `${moment.tz(props.event!.startStr, calendarTZ)
            .tz('UTC')
            .format('YYYY-MM-DD')} ${entry.value.start_hour}`,
        `${
          moment.tz(props.event!.endStr, calendarTZ)
            .tz('UTC')
            .format('YYYY-MM-DD')
        } ${entry.value.end_hour}`
      ]
    } else {
      values.range = [
        `${moment.tz(props.event!.startStr, calendarTZ)
            .tz('UTC')
            .format('YYYY-MM-DD')} ${entry.value.start_hour}`,
        `${
          moment.tz(props.event!.endStr, calendarTZ)
            .tz('UTC')
            .format('YYYY-MM-DD')
        } ${entry.value.end_hour}`
      ]
    }
    values.allDay = values.entry_type?.requires_full_workday ? true : isAllDay(values.range)
    // values.timezone = entry.value.person.timezone ?? 'UTC' // This line will may be used
    values.timezone = entry.value.timezone.id
    if ('excluded_dates' in entry.value) {
      values.excluded_dates = entry.value.excluded_dates
    }

    await nextTick()
    values.repeatFreq = isBlanketEntry.value
      ? 'weekly'
      : entry.value.start_date === entry.value.end_date
        ? 'no-repeat'
        : 'daily'
    values.until = entry.value.end_date ? entry.value.end_date : null
    if ('applied_on_dates' in entry.value) {
      values.applied_on_dates = entry.value.applied_on_dates
    }
    if ('applied_on_days' in entry.value) {
      values.applied_on_days = entry.value.applied_on_days
    }
    if ('applied_on_weeks' in entry.value) {
      values.applied_on_weeks = entry.value.applied_on_weeks
    }
    values.comment = entry.value.comment
    if ('replaces_other_entry' in entry.value) {
      values.replaces_other_entry = entry.value.replaces_other_entry
    }
    if ('replaces_own_entry' in entry.value) {
      values.replaces_own_entry = entry.value.replaces_own_entry
    }
  }
  // Add
  else {
    const calendarAPI = props.calendarRef? props.calendarRef.getApi(): null
    const currentDate = calendarAPI? calendarAPI.getDate(): undefined
    
    const currentTimeFloored = getFlooredTime(moment(currentDate?? '')).tz('UTC')

    values.id = defaultValues.id
    values.person = props.selectionInfo
      ? props.selectionInfo.resource?.extendedProps.person
      : defaultValues.person
    values.entry_type = modeRef.value === 'quick-add-sickness-absence'
      ? values.entry_type
      : defaultValues.entry_type
    values.range = props.selectionInfo
      ? [
          moment(moment.tz(props.selectionInfo.start, calendarTZ).tz('UTC'), 'YYYY-MM-DD HH:mm:ss')
            .format('YYYY-MM-DD HH:mm:ss'),
          moment(moment.tz(props.selectionInfo.end, calendarTZ).tz('UTC'), 'YYYY-MM-DD HH:mm:ss')
            .subtract(props.selectionInfo.allDay ? 1 : 0, 'second')
            .format('YYYY-MM-DD HH:mm:ss')
        ]
      : [
          currentTimeFloored.format('YYYY-MM-DD HH:mm:ss'),
          moment(currentTimeFloored).add(1, 'hour').format('YYYY-MM-DD HH:mm:ss')
        ]
    values.allDay = props.selectionInfo?.allDay ?? defaultValues.allDay
    values.timezone = defaultValues.timezone
    values.repeatFreq = defaultValues.repeatFreq
    values.until = defaultValues.until
    values.applied_on_dates = defaultValues.applied_on_dates
    values.applied_on_days = defaultValues.applied_on_days
    values.applied_on_weeks = defaultValues.applied_on_weeks
    values.comment = defaultValues.comment
    values.replaces_other_entry = defaultValues.replaces_other_entry
    values.replaces_own_entry = defaultValues.replaces_own_entry
  }
  $externalResults.value = {}
  v$.value.$reset()
}

watch(values, () => {
  non_field_errors.value = []
  startOfModal.value = values.range? values.range[0] : entry.value.start_date
})

watch(
  () => values.allDay,
  () => {
    if (!values.allDay && values.range![0] === values.range![1]) {
      values.range![1] = moment(values.range![1]).add(1, 'hour').format('YYYY-MM-DD HH:mm')
    }
  }
)
watch([entryTypes, props], () => {
  modeRef.value = props.mode
  if (props.mode === 'quick-add-sickness-absence' && entryTypes.value) {
    values.entry_type = entryTypes.value.find((entryType) => entryType.name === 'Sick Absence')
  }
})

watch(
  () => untilState.value,
  (isUntil) => {
    if (isUntil === 'never') {
      values.until = null
    }
    v$.value.until.$reset()
  }
)
watch(
  () => values.repeatFreq,
  (frequency) => {
    if(modeRef.value != 'edit') {
      if(frequency === 'weekly') {
        untilState.value = 'never'
      } else {
        untilState.value = 'on'
      }
    }
  }
)

/*
 * Code block to resolve an issue where dates in date-picker calendar
 * become inactive after the calendar has been displayed once
 */
watch(
  () => values.until,
  (until) => {
    if (until === undefined || until === '') {
      values.until = defaultValues.until
    }
  }
)

watch(open, () => {
  if (open.value) {
    resetForm()
  }
})
watchEffect(()=> {
  timezones.value = setLabelSuffix(tzData.value, startOfModal.value)
})
</script>

<template>
  <BModal v-model="open" :no-close-on-backdrop="isPending" centered @hide="emit('hide')">
    <BForm>
      <BAlert
        :model-value="true"
        variant="danger"
        class="mb-[.5rem]"
        v-for="error of non_field_errors"
        :key="error"
      >
        {{ error }}
      </BAlert>

      <div class="flex mb-[.5rem]">
        <label class="col-form-label">
          <span class="icon icon-xs my-1 mx-3 fa fa-solid fa-user"></span>
        </label>
        <div class="flex-1">
          <SelectField
            :loading="isLoadingPeople"
            :options="people"
            label="name"
            v-model="values.person"
            required
            :clearable="false"
            :append-to-body="false"
            placeholder="Please select Team Member"
            class="mb-0"
          />
          <BFormInvalidFeedback :state="!v$.person.$error">
            <div v-for="error of v$.person.$errors" :key="error.$uid">{{ error.$message }}</div>
          </BFormInvalidFeedback>
        </div>
      </div>
      <div class="flex mb-[.5rem]">
        <label class="col-form-label">
          <span class="icon icon-xs my-1 mx-3 fa fa-solid fa-tasks-alt"></span>
        </label>
        <div class="flex-1">
          <SelectField
            :loading="isLoadingEntryTypes"
            :options="entryTypes"
            :selectable="
              (entryType: EntryType) =>
                values.repeatFreq === 'weekly' ? !entryType.is_specific_only : true
            "
            label="name"
            v-model="values.entry_type"
            :clearable="false"
            :append-to-body="false"
            placeholder="Please select Event Type"
            class="mb-0"
            :disabled="mode == 'quick-add-sickness-absence'"
          />
          <BFormInvalidFeedback :state="!v$.entry_type.$error">
            <div v-for="error of v$.entry_type.$errors" :key="error.$uid">{{ error.$message }}</div>
          </BFormInvalidFeedback>
        </div>
      </div>
      <div class="flex mb-[1rem]">
        <label class="col-form-label">
          <span class="icon icon-xs my-1 mx-3 fa fa-solid fa-clock"></span>
        </label>
        <div class="flex-1">
          <div class="mb-[.5rem]">
            <RangePickr
              v-model:range="values.range"
              v-model:timezone="timezoneValue"
              v-model:all-day="values.allDay"
              :timezone-options="timezones"
              :calendar-timezone="calendarTimezone.value"
              :is-loading-timezone-options="isLoadingTimezones"
              :max-diff="24"
              :allday-mandatory="values.entry_type?.requires_full_workday"
              :disabled="mode === 'edit'"
            />
            <BFormInvalidFeedback :state="!v$.range.$error">
              <div v-for="error of v$.range.$errors" :key="error.$uid">
                {{ error.$message }}
              </div>
            </BFormInvalidFeedback>
          </div>

          <div class="mb-[.5rem] w-[180px]">
            <SelectField
              :options="repeatFreqOptions"
              :selectable="
                (option: RepeatFreqOption) =>
                  values.entry_type?.is_specific_only ? option.value !== 'weekly' : true
              "
              :reduce="(option: RepeatFreqOption) => option.value"
              v-model="values.repeatFreq"
              required
              :clearable="false"
              :append-to-body="false"
              :disabled="mode === 'edit'"
              class="mb-0"
            />
          </div>

          <div :class="{ hidden: values.repeatFreq === 'no-repeat' }">
            <BFormGroup
              :label="values.repeatFreq === 'weekly' ? 'Ends' : 'Ends on:'"
              class="mb-[.5rem]"
            >
              <BRow gutter-y="2" class="m-0">
                <BCol class="form-check" cols="12" v-if="values.repeatFreq === 'weekly'">
                  <input
                    type="radio"
                    class="form-check-input"
                    name="repeat-end"
                    id="never-end"
                    v-model="untilState"
                    value="never"
                    :disabled="mode === 'edit'"
                  />
                  <label for="never-end" class="form-check-label"> Never </label>
                </BCol>
                <BCol
                  class="form-check d-flex align-items-center"
                  cols="3"
                  v-if="values.repeatFreq != 'daily'"
                >
                  <div>
                    <input
                      type="radio"
                      class="form-check-input"
                      name="repeat-end"
                      id="end-on"
                      v-model="untilState"
                      value="on"
                      v-if="values.repeatFreq === 'weekly'"
                      :disabled="mode === 'edit'"
                    />
                    <label for="end-on" class="form-check-label"> On </label>
                  </div>
                </BCol>
                <BCol :cols="values.repeatFreq === 'daily' ? 9 : 6" class="p-0">
                  <FlatPickr
                    :config="{
                      minDate: moment(values.range?.[0]).format('YYYY-MM-DD'),
                      allowInput: true,
                      altInput: true,
                      altFormat: 'Y-m-d',
                      locale: { firstDayOfWeek: 1 }
                    }"
                    v-model="values.until"
                    placeholder="End Date"
                    :disabled="untilState === 'never' || mode === 'edit'"
                  />
                </BCol>
              </BRow>
              <BFormInvalidFeedback v-if="untilState === 'on'" :state="!v$.until.$error">
                <div v-for="error of v$.until.$errors" :key="error.$uid">
                  {{ error.$message }}
                </div>
              </BFormInvalidFeedback>
            </BFormGroup>

            <BFormGroup label="Repeat on:" :state="v$.applied_on_dates.$error">
              <template v-if="values.repeatFreq === 'daily'">
                <div class="mb-[.5rem]">
                  <ApplyDatesSelect
                    v-model="values.applied_on_dates"
                    :start_date="values.range?.[0]"
                    :end_date="values.until"
                    :disabled="
                      mode === 'edit' ||
                      !values.range?.[0] ||
                      (untilState === 'on' && !values.until)
                    "
                    placeholder="Please select Applicable Dates"
                  />
                  <BFormInvalidFeedback :state="!v$.applied_on_dates.$error">
                    <div v-for="error of v$.applied_on_dates.$errors" :key="error.$uid">
                      {{ error.$message }}
                    </div>
                  </BFormInvalidFeedback>
                </div>
              </template>
              <template v-else>
                <div class="mb-[.5rem]">
                  <ApplyDaysSelect
                    v-model="values.applied_on_days"
                    :disabled="
                      mode === 'edit' ||
                      !values.range?.[0] ||
                      (untilState === 'on' && !values.until)
                    "
                  />
                  <BFormInvalidFeedback :state="!v$.applied_on_days.$error">
                    <div v-for="error of v$.applied_on_days.$errors" :key="error.$uid">
                      {{ error.$message }}
                    </div>
                  </BFormInvalidFeedback>
                </div>
                <div class="mb-[.5rem]">
                  <ApplyWeeksSelect
                    v-model="values.applied_on_weeks"
                    :start_date="values.range?.[0]"
                    :end_date="values.until"
                    :disabled="mode === 'edit' || !values.range?.[0] || !values.until"
                    placeholder="Please select Applicable Weeks"
                  />
                  <BFormInvalidFeedback :state="!v$.applied_on_weeks.$error">
                    <div v-for="error of v$.applied_on_weeks.$errors" :key="error.$uid">
                      {{ error.$message }}
                    </div>
                  </BFormInvalidFeedback>
                </div>
              </template>
            </BFormGroup>
          </div>
        </div>
      </div>
      <div class="flex mb-0">
        <label class="col-form-label">
          <span class="icon icon-xs my-1 mx-3 fa fa-solid fa-sticky-note"></span>
        </label>
        <div class="flex-1">
          <BFormTextarea v-model="values.comment" rows="3" max-rows="6" placeholder="Comment" />
          <BFormInvalidFeedback :state="!v$.comment.$error">
            <div v-for="error of v$.comment.$errors" :key="error.$uid">
              {{ error.$message }}
            </div>
          </BFormInvalidFeedback>
        </div>
      </div>
    </BForm>

    <template v-slot:ok>
      <BButton type="submit" :disabled="isPending" variant="primary" @click="onSubmit">
        {{ mode === 'edit' ? 'Update' : 'Submit' }}
      </BButton>
    </template>
    <template v-slot:cancel>
      <BButton type="button" variant="danger" @click="onDelete" v-if="mode === 'edit'">
        Delete
      </BButton>
      <BButton type="button" @click="onCancel" v-else>Cancel</BButton>
    </template>
  </BModal>

  <ConfirmModal
    v-model:open="isConfirmModalOpen"
    :is-delete="isDelete"
    :is-blanket-entry="isBlanketEntry"
    @confirm="onConfirm"
  />
</template>

<style scoped lang="scss"></style>
