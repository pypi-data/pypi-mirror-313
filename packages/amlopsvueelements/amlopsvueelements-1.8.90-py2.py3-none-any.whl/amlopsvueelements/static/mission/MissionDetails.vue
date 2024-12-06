<template>
  <FormCard :is-loading="isLoading" add-default-classes>
    <template #header>
      <h2 class="text-[1.25rem] font-medium text-grey-1000">Mission Details</h2>
    </template>
    <template #content>
      <SelectField
        v-model="formModel.organisation"
        required
        label-text="Unit"
        placeholder="Please select Unit"
        :disabled="!!meta"
        :errors="validationInfo?.organisation.$errors"
        :is-validation-dirty="validationInfo?.$dirty"
        label="full_repr"
        :reduce="(item) => ({ id: item.id, full_repr: item.full_repr })"
        :options="organisations"
        :loading="isLoadingOrganisations"
      />
      <SelectField
        v-model="formModel.requesting_person"
        :loading="isLoadingOrganisationPeople"
        :errors="validationInfo?.requesting_person.$errors"
        :options="organisationPeople"
        :reduce="(item) => item.person.id"
        required
        :is-validation-dirty="validationInfo?.$dirty"
        :disabled="!formModel.organisation"
        label="job_title"
        :get-option-label="
          (item) => `${item.person?.details?.first_name} ${item.person?.details?.last_name}`
        "
        label-text="Primary Mission Contact"
        placeholder="Please select Primary Mission Contact"
      />
      <SelectField
        v-model="formModel.type"
        required
        :is-validation-dirty="validationInfo?.$dirty"
        label-text="Mission Type"
        placeholder="Please select Mission Type"
        :errors="validationInfo?.type.$errors"
        label="name"
        :reduce="(item) => item.id"
        :options="requestTypes"
        :loading="isLoadingRequestTypes"
      />
      <InputField
        v-model.uppercase="formModel.callsign"
        :is-validation-dirty="validationInfo?.$dirty"
        :errors="validationInfo?.callsign.$errors"
        required
        label-text="Callsign"
        placeholder="Please enter Callsign"
      />
      <SelectField
        v-model="formModel.aircraft_type"
        :loading="isLoadingAircraftTypes"
        required
        :is-validation-dirty="validationInfo?.$dirty"
        :errors="validationInfo?.aircraft_type.$errors"
        :disabled="!formModel.organisation"
        :options="aircraftTypes"
        :reduce="(item) => +item?.id"
        :get-option-label="
          (item) =>
            `${item?.attributes?.manufacturer} ${item?.attributes?.model} (${item?.attributes?.designator})`
        "
        label-text="Aircraft Type"
        placeholder="Please select Aircraft Type"
      />
      <SelectField
        v-model="formModel.aircraft"
        :is-validation-dirty="validationInfo?.$dirty"
        :loading="isLoadingAircrafts"
        :options="computedFilteredAircrafts"
        :reduce="(item) => item?.id"
        :disabled="!formModel.aircraft_type"
        :get-option-label="(item) => item?.registration"
        label="type.model"
        label-text="Tail Number"
        placeholder=""
      >
        <template #select-option="item">
          {{ item?.registration }}
          <span v-if="item?.operator?.details?.registered_name" class="ml-2 text-grey-400">
            {{ item?.operator?.details?.registered_name }}
          </span>
        </template>
      </SelectField>
      <div>
        <Label :required="false" label-text="Mission Number" />
        <div class="flex">
          <InputField
            v-model="formModel.mission_number_prefix"
            :is-validation-dirty="validationInfo?.$dirty"
            placeholder="Prefix"
            class="w-[250px] mr-[8px]"
          />
          <InputField
            v-model="formModel.mission_number"
            :is-validation-dirty="validationInfo?.$dirty"
            placeholder="Number"
          />
        </div>
      </div>
      <InputField v-if="0" label-text="Unit" placeholder="Please enter Unit" />
      <InputField v-model="formModel.apacs_number" label-text="APACS Number" placeholder="" />
      <InputField
        v-model="formModel.apacs_url"
        :is-validation-dirty="validationInfo?.$dirty"
        :errors="validationInfo?.apacs_url.$errors"
        label-text="APACS URL"
        placeholder=""
      />
      <SelectField
        v-model="formModel.mission_planner"
        :loading="isLoadingOrganisationPeople"
        :options="organisationPeople"
        :reduce="(item) => item.person.id"
        :is-validation-dirty="validationInfo?.$dirty"
        :disabled="!formModel.organisation"
        label="job_title"
        :get-option-label="
          (item) => `${item.person?.details?.first_name} ${item.person?.details?.last_name}`
        "
        label-text="Mission Planner"
        placeholder="Please select Mission Planner"
      />
    </template>
  </FormCard>
</template>

<script lang="ts" setup>
import { computed, onBeforeMount, PropType, watch } from 'vue'
import { FormCard, Label, InputField, SelectField } from 'shared/components'
import { useFetch } from '@/composables/useFetch'
import { ITypeReference } from '@/types/general.types'
import { IOrganisation, IPerson } from '@/types/mission/mission-reference.types'
import { IAircraft } from '@/types/mission/aircraft.types'
import MissionReferences from '@/services/mission/mission-references'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import { storeToRefs } from 'pinia'
import { BaseValidation } from '@vuelidate/core'
import { getIsAdmin } from '@/helpers'

defineProps({
  validationInfo: {
    type: Object as PropType<BaseValidation>,
    default: () => {}
  },
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  }
})

const missionFormStore = useMissionFormStore()

const { formModel } = storeToRefs(missionFormStore)

const {
  loading: isLoadingRequestTypes,
  data: requestTypes,
  callFetch: fetchRequestTypes
} = useFetch<ITypeReference>(async () => {
  return await MissionReferences.fetchHandlingRequestTypes()
})
const {
  loading: isLoadingOrganisationPeople,
  data: organisationPeople,
  callFetch: fetchOrganisationPeople
} = useFetch<IPerson[]>(async (id: number) => {
  return await MissionReferences.fetchOrganisationPeople(id as number)
})
const {
  loading: isLoadingAircraftTypes,
  data: aircraftTypes,
  callFetch: fetchAircraftTypes
} = useFetch<IAircraft[]>(async (id: number) => {
  return await MissionReferences.fetchAircraftTypes(id as number)
})
const {
  loading: isLoadingAircrafts,
  data: aircrafts,
  callFetch: fetchAircrafts
} = useFetch<IAircraft[]>(async (id: number) => {
  return await MissionReferences.fetchAircrafts(id as number)
})
const {
  loading: isLoadingOrganisations,
  data: organisations,
  callFetch: fetchOrganisations
} = useFetch<IOrganisation[]>(async () => {
  return await MissionReferences.fetchOrganisations()
})

// meta for default user
const { data: meta, callFetch: fetchMeta } = useFetch<{ organisation: IOrganisation }>(async () => {
  return await MissionReferences.fetchMeta()
})

watch(
  () => meta.value,
  (meta) => {
    // Set default organisation from user meta
    if (!formModel.value?.organisation && meta?.organisation) {
      formModel.value.organisation = {
        id: meta.organisation.id,
        full_repr: meta.organisation.full_repr
      }
    }
  }
)

const computedFilteredAircrafts = computed(() => {
  if (!formModel.value.aircraft_type) return []
  return (
    (aircrafts.value as IAircraft[])?.filter(
      (aircraft: IAircraft) => `${aircraft?.type?.id}` === `${formModel.value?.aircraft_type}`
    ) ?? []
  )
})

watch(
  () => formModel.value?.organisation?.id,
  async (organisationId: number, oldId) => {
    if (oldId) {
      formModel.value.aircraft = null
      formModel.value.aircraft_type = null
      formModel.value.requesting_person = null
    }
    if (organisationId) {
      return await Promise.allSettled([
        fetchOrganisationPeople(organisationId as any),
        fetchAircraftTypes(organisationId as any),
        fetchAircrafts(organisationId as any)
      ])
    }
  },
  { immediate: true }
)

onBeforeMount(async () => {
  await Promise.allSettled([fetchRequestTypes(), getIsAdmin() ? fetchOrganisations() : fetchMeta()])
})
</script>