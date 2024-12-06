<template>
  <div id="mission-amend-timing" :class="$style['mission-amend-timing']">
    <div
      v-for="error_message in error_messages"
      class="alert alert-danger d-flex align-items-center"
      role="alert"
    >
      <i class="fas fa-exclamation-triangle me-3"></i>
      <div>{{ error_message }}</div>
    </div>
    <div class="p-2">
      <SelectField
        label="label"
        label-text="Mission Leg To Amend"
        placeholder="Please select Flight Leg"
        :options="activeLegs"
        :selectable="(item: any) => !item.disabled"
        :loading="isFetchingMission"
        :clearable="false"
        :append-to-body="false"
        required
        v-model="state.leg"
        :errors="v$.leg.$errors"
        :is-validation-dirty="v$.leg.$dirty"
      />
      <SelectField
        label="label"
        label-text="Movement To Amend"
        placeholder="Please select Movement"
        :options="movements"
        :loading="isFetchingMission"
        :clearable="false"
        :append-to-body="false"
        required
        :disabled="!state.leg"
        v-model="state.movement_direction"
        :errors="v$.movement_direction.$errors"
        :is-validation-dirty="v$.movement_direction.$dirty"
      />
      <Label required label-text="New Movement Date & Time" />
      <FlatPickr
        ref="departureDateRef"
        placeholder="Select date"
        :config="{
          allowInput: true,
          altInput: true,
          altFormat: 'Y-m-d H:i',
          dateFormat: 'Y-m-d H:i',
          enableTime: true,
          time_24hr: true,
          minuteIncrement: 1
        }"
        class="mb-[1rem]"
        required
        :disabled="!state.movement_direction"
        v-model="state.new_datetime"
        :errors="v$.new_datetime.$errors"
        :is-validation-dirty="v$.new_datetime.$dirty"
      />
      <TimeDurationPickr
        :label="changedByLabel"
        requied
        :render-description="renderTimedurationDescription"
        v-model="state.changedBy"
        :disabled="!state.movement_direction"
        :errors="v$.changedBy.$errors"
        :is-validation-dirty="v$.changedBy.$dirty"
      />
      <CheckboxField
        label="change_all_subsequent"
        label-text="Roll Change to All Subsequent Mission Legs?"
        v-model="state.roll_change_to_subsequent_legs"
        :class="$style['flex-reverse']"
        :errors="v$.roll_change_to_subsequent_legs.$errors"
        :is-validation-dirty="v$.roll_change_to_subsequent_legs.$dirty"
      />
    </div>
    <div class="border-b border-b-[#e5e7eb] mt-[25px]"></div>
    <div :class="$style['mission-amend-timing__actions']">
      <div class="flex items-center gap-x-2">
        <button
          data-bs-dismiss="modal"
          type="button"
          class="!bg-gray-200 !text-grey-900"
          :class="[$style['mission-amend-timing__service-btn']]"
        >
          Close
        </button>
        <button
          :class="[
            $style['mission-amend-timing__service-btn'],
            $style['mission-amend-timing__service-btn--submit']
          ]"
          class="!bg-green-700 !text-black-400"
          @click="onSubmit"
        >
          Update Timings
        </button>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, reactive, ref, watchEffect } from 'vue'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import { Label, FlatPickr, TimeDurationPickr, CheckboxField, SelectField } from 'shared/components'
import { useVuelidate } from '@vuelidate/core'
import { required } from '@vuelidate/validators'
import { useFetch } from '@/composables/useFetch'
import Mission from '@/services/mission/mission'
import { notify } from '@/helpers/toast'
import type {
  IAmendTiming,
  IExtendedMission,
  IExtendedMissionLeg
} from '@/types/mission/mission.types'
import { getMissionId, redirectToURL } from '@/helpers'

dayjs.extend(utc)

const {
  data: mission,
  loading: isFetchingMission,
  callFetch: fetchMission
} = useFetch<IExtendedMission, (missionId: number) => Promise<IExtendedMission>>(
  async (missionId: number) => {
    const { data } = await Mission.getMission(missionId)

    return data
  }
)

const activeLegs = computed(() => {
  if (!mission.value) {
    return []
  }

  const sortedLegs = mission.value.legs?.sort((a, b) => a.sequence_id - b.sequence_id)

  return sortedLegs.map((leg: IExtendedMissionLeg) => ({
    label: `Flight Leg ${leg.sequence_id} - ${leg.departure_location.tiny_repr}>${leg.arrival_location.tiny_repr}`,
    value: leg.id,
    disabled: dayjs.utc(leg.arrival_datetime).isBefore(dayjs.utc())
  }))
})

const movements = computed(() => {
  if (!state.leg?.value) {
    return []
  }

  const selectedLeg = mission.value?.legs.find(
    (leg: IExtendedMissionLeg) => leg.id === state.leg.value
  )

  if (!selectedLeg) {
    return []
  }

  return [
    {
      //   label: `Departure - ${selectedLeg.departure_datetime}`,
      label: `Departure - ${dayjs
        .utc(selectedLeg.departure_datetime)
        .format('MMM-DD-YYYY HH:mm')}Z`,
      datetime: selectedLeg.departure_datetime,
      value: 'departure'
    },
    {
      //   label: `Arrival - ${selectedLeg.arrival_datetime}`,
      label: `Arrival - ${dayjs.utc(selectedLeg.arrival_datetime).format('MMM-DD-YYYY HH:mm')}Z`,
      datetime: selectedLeg.arrival_datetime,
      value: 'arrival'
    }
  ]
})

const state = reactive<any>({
  leg: null,
  movement_direction: null,
  new_datetime: null,
  changedBy: null,
  roll_change_to_subsequent_legs: false
})

const rules = computed(() => ({
  leg: {
    required
  },
  movement_direction: {
    required
  },
  new_datetime: {
    required
  },
  changedBy: {
    required
  },
  roll_change_to_subsequent_legs: { required }
}))

const $externalResults = ref({})

const error_messages = ref<string[]>([])

const changedByLabel = computed(() => {
  return state.changedBy === undefined
    ? 'Movement changed By'
    : state.changedBy > 0
    ? 'Movement Delayed By'
    : 'Movement Brought Forward by'
})

const renderTimedurationDescription = (value: number | null) => {
  if (!value) return ''

  value = Math.abs(value)
  const hours = value ? Math.trunc(dayjs.duration(value).asHours()) : 0
  const minutes = value ? dayjs.duration(value).minutes() : 0

  return `${hours} hours and ${minutes} minutes`
}

watchEffect(() => {
  if (!state.new_datetime || !state.movement_direction) {
    return
  }

  state.changedBy = dayjs.utc(state.new_datetime).diff(dayjs.utc(state.movement_direction.datetime))
})

watchEffect(() => {
  if (state.changedBy === null || !state.movement_direction) {
    return
  }

  state.new_datetime = dayjs
    .utc(state.movement_direction.datetime)
    .add(state.changedBy)
    .format('YYYY-MM-DD HH:mm')
})

const v$ = useVuelidate(rules, state, { $externalResults })

const onSubmit = async () => {
  const isValid = await v$?.value?.$validate()

  if (!isValid) {
    return
  }

  const amend_timinng: IAmendTiming = {
    movement_direction: state.movement_direction.value,
    new_datetime: state.new_datetime,
    roll_change_to_subsequent_legs: state.roll_change_to_subsequent_legs
  }

  try {
    await Mission.putMissionAmendTiming(state.leg.value, amend_timinng)
    redirectToURL(getMissionId() as number)
  } catch (error: any) {
    if (error.response) {
      const { errors } = error.response.data

      if (errors.length > 0 && typeof errors[0] === 'string') {
        error_messages.value = errors
      } else {
        $externalResults.value = {
          movement_direction: errors.movement_direction?.map((err: any) => err.detail),
          new_datetime: errors.new_datetime?.map((err: any) => err.detail),
          roll_change_to_subsequent_legs: errors.roll_change_to_subsequent_legs?.map(
            (err: any) => err.detail
          )
        }
      }
    }
  }
}

const fetchData = () => {
  const missionId = getMissionId() as number
  fetchMission(missionId)
}

onMounted(fetchData)
</script>
<style scoped lang="scss"></style>

<style module lang="scss">
.mission-amend-timing {
  @apply relative flex flex-col bg-white min-w-0 rounded-[0.5rem] pb-2;

  .flex-reverse {
    flex-direction: row-reverse;
    justify-content: flex-end;
    align-items: flex-start;
    margin-top: 2px;
    column-gap: 8px;
  }

  &__actions {
    @apply flex items-center justify-end mt-2 px-2;
  }

  &__service-btn {
    @apply text-sm flex shrink-0 focus:shadow-none rounded-md text-white mb-0 mt-2 p-2 px-4 w-fit #{!important};

    &--primary {
      @apply bg-grey-900 #{!important};
    }

    &--submit {
      @apply bg-confetti-500 text-gray-900 #{!important};
    }
  }
}
</style>