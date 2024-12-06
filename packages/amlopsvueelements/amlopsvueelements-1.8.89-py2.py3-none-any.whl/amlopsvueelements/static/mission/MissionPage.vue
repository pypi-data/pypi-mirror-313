<template>
  <div>
    <MissionDetails
      :is-loading="isLoading"
      class="mb-3 min-w-[540px]"
      :validation-info="v$?.form"
    />
    <MissionItinerary :is-loading="isLoading" :validation-info="v$?.form" class="overflow-x-auto" />
    <ErrorBox v-if="formErrors.length || Object.keys(formErrors)?.length" class="mb-3" />
    <div class="pb-[3.75rem] flex items-center gap-x-2">
      <Button :class="[$style['ops-page-wrapper__btn']]" :loading="isLoading" @click="onValidate">
        <span>{{ computedTitleSubmit }}</span>
      </Button>
      <Button :class="[$style['ops-page-wrapper__go-back']]" @click="goBack">
        <span>Back</span>
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import MissionDetails from '@/components/forms/sections/MissionDetails.vue'
import MissionItinerary from '@/components/forms/sections/MissionItinerary.vue'
import { Button } from 'shared/components'
import { storeToRefs } from 'pinia'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import useVuelidate from '@vuelidate/core'
import { useFetch } from '@/composables/useFetch'
import type { Nullable } from '@/types/generic.types'
import type { IMissionFormStructure } from '@/types/mission/mission.types'
import Mission from '@/services/mission/mission'
import { rules } from '@/utils/rulesForForms'
import { useMissionStore } from '@/stores/useMissionStore'
import { computed, nextTick, onMounted } from 'vue'
import { getMissionId, redirectToURL } from '@/helpers'
import { notify } from '@/helpers/toast'
import ErrorBox from '@/components/forms/ErrorBox.vue'
import { mapFormMission } from '@/helpers/mission'
import dayjs from 'dayjs'
import { calculateLegHeight } from '@/composables/mission/useCalculateLegHeight'

const missionFormStore = useMissionFormStore()
const missionStore = useMissionStore()
const { formModel: missionForm, formErrors } = storeToRefs(missionFormStore)
const { isUpdatingMission } = storeToRefs(missionStore)

const v$ = useVuelidate(rules(missionForm), { form: missionForm.value })
const computedTitleSubmit = computed(() => {
  return getMissionId() ? 'Update mission' : 'Submit mission'
})

const {
  loading: isCreatingMission,
  data: createdMissionData,
  callFetch: createMission
} = useFetch(async (payload: Nullable<IMissionFormStructure>) => {
  const mappedPayload = mapFormMission(payload)
  const res = await Mission.create(mappedPayload)
  redirectToURL(res.data.id)
  notify('Mission created successfully!', 'success')
  return res
})

const isLoading = computed(() => isCreatingMission?.value || isUpdatingMission?.value)

onMounted(() => {
  getMissionId() && missionStore.fetchMission(getMissionId() as number)
})

const missionActions = async () => {
  const mappedLegs = missionForm.value.legs.map((leg) => {
    return {
      ...leg,
      arrival_datetime: dayjs(leg.arrival_datetime).format(
        `YYYY-MM-DD[T]HH:mm:ss${leg.arrival_datetime_is_local ? '' : '[Z]'}`
      ),
      departure_datetime: dayjs(leg.departure_datetime).format(
        `YYYY-MM-DD[T]HH:mm:ss${leg.departure_datetime_is_local ? '' : '[Z]'}`
      )
    }
  })
  const mappedMission = {
    ...missionForm.value,
    legs: mappedLegs
  }
  return getMissionId()
    ? await missionStore.updateMission(getMissionId() as number, mappedMission)
    : await createMission(mappedMission as any)
}

const onValidate = async () => {
  try {
    const isValid = await v$?.value?.$validate()
    if (!isValid) {
      return notify('Error while submitting, form is not valid!', 'error')
    } else {
      await missionActions()
      formErrors.value = []
    }
  } catch (error) {
    if (error.response?.data?.errors?.some((err) => typeof err === 'string')) {
      return (formErrors.value = error.response?.data?.errors)
    }
  }
}
const goBack = () => {
  window?.history?.go(-1)
}
</script>

<style lang="scss" module>
.ops {
  &-page-wrapper {
    @apply flex justify-between items-center gap-2 mb-4;

    &__btn {
      @apply flex shrink-0 focus:shadow-none text-white bg-grey-900 mb-0 mt-2 p-2 px-4 #{!important};

      img {
        @apply w-5 h-5 mr-2;
        filter: invert(36%) sepia(14%) saturate(1445%) hue-rotate(190deg) brightness(93%)
          contrast(84%);
      }
    }

    &__go-back {
      @apply flex shrink-0 focus:shadow-none text-grey-900 bg-grey-75 mb-0 mt-2 p-2 px-4 #{!important};
    }

    &__content {
      @apply pr-0 sm:pr-4 sm:mr-[-1rem] relative;
    }
  }
}
</style>