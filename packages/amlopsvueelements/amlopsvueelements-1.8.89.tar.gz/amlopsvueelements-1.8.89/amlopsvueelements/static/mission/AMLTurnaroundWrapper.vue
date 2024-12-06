<template>
  <div :class="[$style['ops-aml-turnaround-wrapper']]">
    <div :class="[$style['ops-aml-turnaround__content']]">
      <div :class="$style['ops-aml-turnaround__servicing-checkbox']">
        <img class="mb-4 w-full !max-w-[7rem] !block mx-auto" :src="amlLogo" alt="logo" />
        <div @click.stop.prevent.capture="onHandleAmlServicing">
          <CheckboxField
            :model-value="isAmlServicingEnabled"
            class="!mb-0 !gap-y-4 flex flex-col text-center"
          >
            <template #label>
              <div class="text-base cursor-pointer">
                <p>AML Servicing</p>
                <p>at {{ arrivalAirportShortName }}</p>
              </div>
            </template>
          </CheckboxField>
        </div>
      </div>
      <div class="!min-h-[29.5rem] w-full pb-[1.375rem] relative px-4">
        <div v-if="missionFormModel.legs[legIndex]?.servicing" class="h-full">
          <p class="text-center !font-medium !py-4">
            Fueling
            <span v-if="arrivalAirportShortName">- {{ arrivalAirportShortName }}</span>
          </p>
          <div class="flex items-center">
            <p class="text-base whitespace-nowrap min-w-[9rem]">Fuel required:</p>
            <SelectField
              v-model="missionFormModel.legs[legIndex].servicing.fuel_required"
              :disabled="isDisabledField"
              :options="FuelRequiredTypes"
              :reduce="(item) => item.value"
              label="label"
              class="!mb-0"
              @update:model-value="onChangeFuellingType"
            />
          </div>
          <div class="flex items-center mt-4">
            <p class="text-base whitespace-nowrap min-w-[9rem]">Quantity:</p>
            <InputField
              v-model="missionFormModel.legs[legIndex].servicing.fuel_quantity"
              :disabled="isDisabledField || isFuelingDisabled"
              type="number"
              class="!mb-0"
              label="attributes.description"
            />
          </div>
          <div class="flex items-center mt-4">
            <p class="text-base whitespace-nowrap min-w-[9rem]">Unit of Measure:</p>
            <SelectField
              :model-value="missionFormModel.legs[legIndex].servicing.fuel_unit"
              :required="!isFuelingDisabled"
              placeholder="Please select Unit of Measure"
              :loading="isLoadingQuantityUnits"
              :options="quantityUnits"
              :errors="fuelErrors"
              :is-validation-dirty="isValidationDirty"
              :get-option-label="(item) => `${item.description_plural} (${item?.code})`"
              :reduce="(item) => item.id"
              :disabled="isDisabledField || isFuelingDisabled"
              position="top"
              class="!mb-0"
              @update:model-value="onUpdateFuelUnit"
            />
          </div>
          <div class="flex items-center justify-between mt-4">
            <div class="flex items-center">
              <p class="text-base whitespace-nowrap min-w-[9rem]">Prist required?</p>
              <CheckboxField
                v-model="missionFormModel.legs[legIndex].servicing.fuel_prist_required"
                :disabled="isDisabledField"
                class="mb-0"
              />
            </div>
          </div>
          <div class="!py-4">
            <p class="text-center !font-medium">
              Servicing
              <span v-if="arrivalAirportShortName">- {{ arrivalAirportShortName }}</span>
            </p>
          </div>

          <div class="flex justify-between my-2">
            <div class="items-center">
              <label class="text-base whitespace-nowrap min-w-[9rem]">Ground Handling Required<input type="checkbox" hidden v-model="groundHandlingRequired"></label>
            </div>
            <div
              class="border-b self-end mb-1 border-dashed border-grey-opacity-800/25 h-1 w-full mx-3"
            />
            <div>
              <CheckboxField
                v-model="groundHandlingRequired"
                :disabled="!groundHandlingToggleActive"
                class="mb-0"
                :class="{'opacity-75': !groundHandlingToggleActive}"
              />
            </div>
          </div>
          
          <div v-if="groundHandlingRequired"  class="flex items-center justify-between pb-4">
            <p class="text-base font-medium">Selected services</p>
            <div class="flex mr-2">
              <div
                v-if="missionFormModel.legs[legIndex].servicing.services?.length"
                class="flex gap-x-[0.5rem] justify-between font-normal text-base items-center"
              >
                <span>Arr</span>
                <span>Dep</span>
              </div>
            </div>
          </div>
          <div class="flex font-medium text-[1.25rem] text-grey-1000">
            <div class="flex flex-col items-center w-full">
              <div class="w-full relative">
                <SelectField
                  v-if="groundHandlingRequired" 
                  v-model="missionFormModel.legs[legIndex].servicing.services"
                  class="max-w-[310px] w-[76%] !mb-2"
                  placeholder="Select service"
                  multiple
                  hide-values
                  :disabled="isDisabledField"
                  :loading="isLoadingServices"
                  :options="computedFilteredServiceOptions"
                  position="top"
                  :clearable="false"
                  :get-option-id="(item) => item.id"
                  :get-option-label="
                    (item) => {
                      if (item?.attributes) return item?.attributes?.name
                      return serviceOptions?.find((option) => option.id === item.service)
                        ?.attributes?.name
                    }
                  "
                  :reduce="
                    (item) => {
                      if (!item?.attributes) return item
                      return {
                        service: item?.id,
                        on_arrival: false,
                        on_departure: false,
                        is_allowed_free_text: item?.attributes?.is_allowed_free_text,
                        is_allowed_quantity_selection:
                          item?.attributes?.is_allowed_quantity_selection,
                        quantity_selection_uom: item?.attributes?.quantity_selection_uom,
                        note: '',
                        booking_text: '',
                        booking_quantity: null
                      }
                    }
                  "
                  @search="onSearchPrist"
                />
                <div
                  v-if="
                    missionFormModel.legs[legIndex].servicing.services?.length && !searchPristQuery
                  "
                  class="pointer-events-none absolute text-base top-2.5 text-grey-200 font-light left-4"
                >
                  Select service
                </div>
              </div>
              <div
                v-if="missionFormModel.legs[legIndex]?.servicing?.services?.length"
                class="flex flex-col gap-y-[0.5rem] w-full border border-grey-100 rounded-md p-2"
              >
                <div
                  v-for="(service, index) in missionFormModel.legs[legIndex].servicing.services"
                  :key="service.id"
                  class="w-full last:!border-none"
                >
                  <div class="flex items-center justify-between w-full">
                    <div class="flex items-center shrink-0 whitespace-nowrap h-[22px]">
                      <div class="flex items-center w-full">
                        <img
                          :class="[$style['ops-aml-turnaround__content__delete-icon']]"
                          :src="getImageUrl(`assets/icons/close-circle-outline.svg`)"
                          alt="disapprove"
                          @click="onRemoveService(index, service.service)"
                        />

                        <Tooltip>
                          <template #target>
                            <Label
                              :class="
                                service.is_allowed_quantity_selection ||
                                (service.is_allowed_free_text && 'max-w-[7rem]')
                              "
                              text-class="mb-0 text-sm truncate"
                              :required="false"
                              :label-text="findServiceById(service.service, serviceOptions).name"
                            />
                          </template>
                          <template #popper>
                            {{ findServiceById(service.service, serviceOptions).name }}
                          </template>
                        </Tooltip>
                      </div>
                    </div>
                    <div
                      v-if="service.is_allowed_quantity_selection || service.is_allowed_free_text"
                      :class="[
                        $style['ops-aml-turnaround__content__free-input'],
                        $style['free-input'],
                        ...(servicesError?.$response?.extraParams?.services?.[index]?.error &&
                        isValidationDirty
                          ? [$style['free-input__error']]
                          : [])
                      ]"
                    >
                      <input
                        v-if="service.is_allowed_free_text"
                        v-model="service.booking_text"
                        placeholder="Description"
                        maxlength="255"
                        type="text"
                      />
                      <input
                        v-if="service.is_allowed_quantity_selection"
                        v-model="service.booking_quantity"
                        placeholder="Quantity"
                        type="number"
                        min="0"
                      />
                      <span class="lowercase" :class="$style['free-input__prefix']">
                        {{ service?.quantity_selection_uom?.code }}
                      </span>
                    </div>
                    <div
                      v-if="!service.is_allowed_free_text && !service.is_allowed_quantity_selection"
                      class="border-b self-end mb-1 border-dashed border-grey-opacity-800/25 h-1 w-full mx-3"
                    />

                    <VMenu
                      :triggers="['click', 'focus']"
                      :popper-triggers="['click', 'focus']"
                      placement="top-start"
                      class="mr-2"
                    >
                      <img
                        :class="[$style['ops-aml-turnaround__content__comment-icon']]"
                        :src="getImageUrl(`assets/icons/comment-alt-regular.svg`)"
                        alt="comment"
                      />
                      <template #popper>
                        <div class="mt-2 px-4">
                          <InputField v-model="service.note" label-text="Comments:" />
                        </div>
                      </template>
                    </VMenu>
                    <div class="flex justify-between gap-x-[0.5rem] items-center pr-1">
                      <CheckboxField
                        v-model="service.on_arrival"
                        :disabled="
                          isDisabledField ||
                          !findServiceById(
                            service.service,
                            serviceOptions,
                            missionFormModel.legs[legIndex]?.arrival_location.id
                          ).arrival
                        "
                        class="!mb-0 d-flex"
                        size="24px"
                      />
                      <CheckboxField
                        v-model="service.on_departure"
                        :disabled="
                          isDisabledField ||
                          !findServiceById(
                            service.service,
                            serviceOptions,
                            missionFormModel.legs[legIndex]?.arrival_location.id
                          ).departure
                        "
                        class="gap-0 !mb-0"
                        size="24px"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="h-full relative">
          <div :class="[$style['ops-aml-turnaround__error']]">Servicing is disabled</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { computed, onMounted, PropType, ref, watch, watchEffect } from 'vue'
import { getHost, getImageUrl } from '@/helpers'
import { Tooltip, Label, InputField, CheckboxField, SelectField } from 'shared/components'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import { storeToRefs } from 'pinia'
import { FuelRequiredTypes, missionLegServicingDefaults } from '@/constants/mission.constants'
import { useFetch } from '@/composables/useFetch'
import { useMissionReferenceStore } from '@/stores/useMissionReferenceStore'
import MissionReferences from '@/services/mission/mission-references'
import { ErrorObject } from '@vuelidate/core'
import type { IService } from '@/types/mission/mission-reference.types'
import { IAirport } from '@/types/mission/airport.types'
import type { ILegService, ServiceFuelingType } from '@/types/mission/mission.types'
import { getMissionId } from '@/helpers'
import { findServiceById } from '@/helpers/mission'

const props = defineProps({
  legSequenceId: {
    type: Number,
    default: 0
  },
  legIndex: {
    type: Number,
    default: 0
  },
  leg: {
    type: Object,
    default: () => ({})
  },
  errors: {
    type: Object as PropType<Record<string, ErrorObject[]>>,
    default: () => ({})
  },
  isValidationDirty: {
    type: Boolean,
    default: false
  }
})

const missionFormStore = useMissionFormStore()
const missionReferenceStore = useMissionReferenceStore()
const { isLoadingQuantityUnits, quantityUnits } = storeToRefs(missionReferenceStore)
const { formModel: missionFormModel } = storeToRefs(missionFormStore)
const missionsReferenceStore = useMissionReferenceStore()
const { selectedDestinationAirportsLeg } = storeToRefs(missionsReferenceStore)
const searchPristQuery = ref('')
const groundHandlingRequired = ref(true)
const groundHandlingToggleActive = ref(true)

const amlLogo = `${getHost()}/static/assets/img/aml_logo_simple_65.png`

const {
  loading: isLoadingServices,
  data: serviceOptions,
  callFetch: fetchServices
} = useFetch<IService[], (locationId: number, organisationId?: number) => void>(
  async (locationId: number, organisationId?: number) => {
    const data = await MissionReferences.fetchServices(locationId, organisationId)
    return data
  }
)
const { callFetch: fetchAirportLocations } = useFetch<IAirport[], (search?: string) => void>(
  async (search?: string) => {
    return await MissionReferences.fetchAirportLocations(search)
  }
)

const computedFilteredServiceOptions = computed<IService[]>(() => {
  if (!serviceOptions.value?.length) return []
  return serviceOptions.value?.filter((option: IService) => {
    return !(computedLegInfo.value?.servicing?.services as ILegService[])?.some((service) => {
      return Number(service?.service) === Number(option.id)
    })
  })
})

const computedLegInfo = computed(() => missionFormModel.value?.legs?.[props.legIndex])

const isAmlServicingEnabled = computed<boolean>(
  () => computedLegInfo.value.arrival_location && computedLegInfo.value.arrival_aml_service
)

const fuelErrors = computed(() => {
  return props.errors?.servicing.filter((error) => error.$validator === 'fuel_unit')
})

const servicesError = computed(() => {
  return props.errors?.servicing?.filter(
    (error) => error.$validator === 'servicesDescriptionValidator'
  )?.[0]
})

const onHandleAmlServicing = () => {
  if (getMissionId() && props.leg?.sequence_id !== undefined) {
    isAmlServicingEnabled.value ? onCancelServicing() : onToggleAmlServicing(true)
    return
  }
  return onToggleAmlServicing(!isAmlServicingEnabled.value)
}
const arrivalAirportShortName = computed(() => {
  if (selectedDestinationAirportsLeg.value && selectedDestinationAirportsLeg.value.length){
    return (
      (selectedDestinationAirportsLeg.value &&
        selectedDestinationAirportsLeg.value?.find((airport: IAirport) => {
          return airport?.id === computedLegInfo.value?.arrival_location?.id ? airport : ''
        })?.tiny_repr) ||
      ''
    )
  } else if(missionFormModel.value.legs && missionFormModel.value.legs.length) {
    const currentLeg = missionFormModel.value.legs.find(airport => 
    airport!.arrival_location?.id != null && computedLegInfo.value!.arrival_location?.id != null &&
        airport!.arrival_location!.id === computedLegInfo.value!.arrival_location!.id
    )

    return (currentLeg && currentLeg.arrival_location?.tiny_repr) ? currentLeg.arrival_location?.tiny_repr : '' 
  } else {
    return ''
  }
})

const isDisabledField = computed(() => {
  return !isAmlServicingEnabled.value || !computedLegInfo.value?.arrival_location
})

const isFuelingDisabled = computed(() => computedLegInfo.value?.servicing.fuel_required === null)

const onToggleAmlServicing = (flag: boolean) => {
  missionFormModel.value.legs[props.legIndex].arrival_aml_service = flag
  if (flag) {
    const lastFuelRequiredLeg = [...missionFormModel.value.legs]
      .splice(0, props.legIndex)
      .findLast((el) => el?.servicing?.fuel_required)
    const DEFAULT_FUEL_UNIT_ID = 5

    return (missionFormModel.value.legs[props.legIndex].servicing = {
      ...missionLegServicingDefaults(),
      fuel_unit: lastFuelRequiredLeg?.servicing?.fuel_unit || DEFAULT_FUEL_UNIT_ID
    })
  }
  delete missionFormModel.value.legs[props.legIndex].servicing
}

const onChangeFuellingType = (type: ServiceFuelingType) => {
  if (type === null) {
    missionFormModel.value.legs[props.legIndex].servicing.fuel_quantity = 0
    missionFormModel.value.legs[props.legIndex].servicing.fuel_unit = null
  }
}
const onCancelServicing = async () => {
  const { isConfirmed } = await window.Swal({
    title: 'Confirmation',
    text: `Please confirm that you wish cancel the servicing & fueling arrangements at ${
      arrivalAirportShortName.value
    } for legs ${props.legIndex + 1} & ${props.legIndex + 2}`,
    icon: 'info',
    showCancelButton: true
  })
  if (isConfirmed) {
    onToggleAmlServicing(false)
  }
}

const onRemoveService = (serviceIndex: number) => {
  missionFormModel.value.legs[props.legIndex].servicing?.services.splice(serviceIndex, 1)
}

const onSearchPrist = (event: string) => {
  searchPristQuery.value = event
}
const fillSelectedDestinationAirports = () => {
  const legs = missionFormModel.value.legs
  legs?.forEach(async (leg) => {
    const destinationAirportFullName = leg.arrival_location?.full_repr
    const data: IAirport[] | any = await fetchAirportLocations(
      destinationAirportFullName?.slice(0, 10)
    )
    selectedDestinationAirportsLeg.value.push(...data)
  })
}
watch(
  () => [computedLegInfo.value?.arrival_location, missionFormModel.value?.organisation],
  async ([location, organisation], [oldLocation]) => {
    if (
      !!oldLocation &&
      location?.id !== oldLocation?.id &&
      missionFormModel.value.legs[props.legIndex]?.servicing
    ) {
      missionFormModel.value.legs[props.legIndex].servicing.services = []
    }
    if (getMissionId()) {
      fillSelectedDestinationAirports()
    }
    await fetchServices(location?.id, organisation?.id)
  }
)
watch(groundHandlingRequired, (ghrValue) => {
  if(!ghrValue) {
    const services = missionFormModel.value.legs?.[props.legIndex]?.servicing?.services
    if(services) {
      missionFormModel.value.legs?.[props.legIndex]?.servicing?.services?.splice(0, services.length)
    }
  }
})

watchEffect(()=> {
  const legs = missionFormModel.value.legs
  const currentLeg = legs![props.legIndex]
  const prevLeg = legs![props.legIndex - 1]
  const nextLeg = legs![props.legIndex + 1]
  
  if(currentLeg?.servicing?.services?.length) {
    currentLeg.servicing.services.forEach((curService) => {
      if(curService?.service === 29) {
        let prevPob_pax, nextPob_pax = false

        prevLeg?.servicing?.services?.forEach(prevService => {
          if (prevService?.service === 29)
            prevPob_pax = prevService.on_departure === true
        })
        if(!curService.on_arrival && !prevPob_pax) currentLeg.pob_pax = null

        nextLeg?.servicing?.services?.forEach((nextService) => {
          if(nextService?.service === 29)
            nextPob_pax = nextService.on_arrival === true
        })
        if(!curService.on_departure && !nextPob_pax) nextLeg!.pob_pax = null
      }
    })
  }
})


const onUpdateFuelUnit = (value) => {
  missionFormModel.value.legs[props.legIndex].servicing.fuel_unit = value
  if (missionFormModel.value.legs.length) {
    missionFormModel.value.legs = missionFormModel.value.legs.map((leg, index) => {
      const isServicingExist = typeof leg?.servicing === 'object'
      const isFuelRequired = leg?.servicing?.fuel_required
      return index >= props.legIndex && isServicingExist && isFuelRequired
        ? {
            ...leg,
            servicing: { ...leg.servicing, fuel_unit: value }
          }
        : leg
    })
  }
}
onMounted(() => {
  if (props.leg) {
    if(props.leg.id) {
      !props.leg.servicing?.is_ground_handling_required && (groundHandlingToggleActive.value = true)
      props.leg.servicing?.is_ground_handling_required && (groundHandlingToggleActive.value = false)
    } else {
      groundHandlingToggleActive.value = true
    }
  }

  if (!computedLegInfo.value?.arrival_location && !missionFormModel.value?.organisation) return
  fetchServices(
    computedLegInfo.value?.arrival_location?.id,
    missionFormModel.value?.organisation?.id as any
  )
})
</script>
<style scoped lang="scss">
.v-popper--theme-menu {
  @apply shrink-0;
}
</style>
<style lang="scss" module>
.ops-aml-turnaround-wrapper {
  @apply h-full;
}

.ops-aml-turnaround {
  &-wrapper {
    @apply flex rounded-[0.5rem] flex-col bg-white min-w-0 px-0 #{!important};
  }

  &__content {
    @apply flex font-medium text-[1.25rem] h-auto  text-grey-1000 h-full;
    &__delete-icon {
      @apply w-[18px] mr-1 cursor-pointer aspect-square;
      filter: invert(23%) sepia(85%) saturate(2552%) hue-rotate(330deg) brightness(87%)
        contrast(103%);
    }

    &__comment-icon {
      @apply w-[20px] h-[20px] shrink-0 cursor-pointer aspect-square;
      filter: invert(17%) sepia(18%) saturate(1710%) hue-rotate(179deg) brightness(96%)
        contrast(95%);
    }

    .free-input {
      @apply mx-2 pl-2 leading-6 w-full h-fit overflow-hidden flex items-center appearance-none text-[0.875rem] bg-clip-padding  bg-white font-normal focus:outline-none text-grey-700 border-grey-100 border-[0.0625rem] border-solid rounded-[0.5rem] #{!important};

      input {
        @apply border-0 shadow-none outline-none w-full #{!important};
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.07);
        transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
      }

      &__prefix {
        @apply bg-grey-50 px-2;
      }

      &__error {
        @apply border-red-500 #{!important};
      }
    }
  }

  &__servicing-checkbox {
    @apply flex flex-col justify-center items-center border-r border-grey-opacity-800/25 min-w-[10rem] px-2;
  }

  &__error {
    @apply absolute z-50 opacity-100 text-[14px] text-[#97650e] w-[97%] text-center p-4 rounded-[0.5rem] top-1/2 right-0 -translate-y-[25%] border-[#fee5ba] bg-[#feeed1];
  }
}
</style>