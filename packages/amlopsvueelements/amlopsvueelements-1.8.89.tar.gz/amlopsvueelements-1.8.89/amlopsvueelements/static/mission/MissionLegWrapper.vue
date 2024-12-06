<template>
  <div :class="[$style['mission-leg-wrapper']]">
    <div :class="[$style['mission-leg-wrapper__content']]">
      <AirportLocationApiSelectField
        v-model="missionFormModel.legs[legIndex].departure_location"
        :errors="errors?.departure_location"
        :is-validation-dirty="isValidationDirty"
        required
        label-text="Departure Airport:"
        placeholder="Please select Departure Airport"
        @update:model-value="onChangeDepartureLocation"
      />
      <div class="flex flex-col mb-4 lg:mb-0">
        <div class="flex items-start gap-x-2 w-full">
          <div class="w-6/12 min-w-[132px]">
            <Label required label-text="Departure Date:" class="whitespace-nowrap" />
            <FlatPickr
              ref="departureDateRef"
              v-model="dateTime.departureDate"
              :errors="errors?.departure_datetime"
              :is-validation-dirty="isValidationDirty"
              :config="{
                allowInput: true,
                altInput: true,
                altFormat: 'Y-m-d',
                dateFormat: 'Y-m-d',
                minDate: computedMinimumDepartureDate
              }"
              @on-change="(...args) => onChangeDepartureDate(args)"
              @on-close="onCloseCalendar"
            />
          </div>
          <div class="w-3/12">
            <Label required label-text="Time:" class="whitespace-nowrap" />
            <FlatPickr
              v-model="dateTime.departureTime"
              placeholder="Time"
              :errors="errors?.departure_datetime"
              :is-validation-dirty="isValidationDirty"
              :config="{
                altFormat: 'H:i',
                altInput: true,
                allowInput: true,
                noCalendar: true,
                enableTime: true,
                time_24hr: true,
                minTime: computedMinimumDepartureTime,
                minuteIncrement: 1
              }"
              class="!pr-0"
              @on-change="(...args) => onChangeDepartureHours(args)"
              @on-close="onCloseCalendar"
            />
          </div>
          <div class="w-3/12">
            <Label :required="false" label-text="Timezone:" class="whitespace-nowrap" />
            <SelectField
              :model-value="missionFormModel.legs[legIndex].departure_datetime_is_local"
              :options="[
                { label: 'UTC', value: false },
                { label: 'Local', value: true }
              ]"
              :reduce="(item) => item.value"
              :clearable="false"
              :disabled="!missionFormModel.legs[legIndex].departure_location?.is_lat_lon_available"
              label="label"
              placeholder="Timezone"
              class="timezone-select mb-0 re-css"
              :append-to-body="false"
              @update:model-value="onChangeTimeZone('departure_datetime_is_local', $event)"
            />
          </div>
        </div>
      </div>
      <AirportLocationApiSelectField
        v-model="missionFormModel.legs[legIndex].arrival_location"
        :errors="errors?.arrival_location"
        :is-validation-dirty="isValidationDirty"
        required
        label-text="Destination Airport:"
        placeholder="Please select Destination Airport"
        @update:model-value="onChangeArrivalLocation"
      />
      <div class="flex flex-col mb-4 lg:mb-0">
        <div class="flex items-start gap-x-2 w-full">
          <div class="w-6/12 min-w-[132px]">
            <Label required label-text="Arrival Date:" class="whitespace-nowrap" />
            <FlatPickr
              v-model="dateTime.arrivalDate"
              :errors="errors?.arrival_datetime"
              :is-validation-dirty="isValidationDirty"
              :config="{
                allowInput: true,
                altInput: true,
                altFormat: 'Y-m-d',
                dateFormat: 'Y-m-d',
                minDate: computeMinimumArrivalDate,
                minuteIncrement: 1
              }"
              @on-change="(...args) => onChangeArrivalDate(args)"
              @on-close="onCloseCalendar"
            />
          </div>
          <div class="w-3/12">
            <Label required label-text="Time:" class="whitespace-nowrap" />
            <FlatPickr
              v-model="dateTime.arrivalTime"
              placeholder="Time"
              :errors="errors?.arrival_datetime"
              :is-validation-dirty="isValidationDirty"
              :config="{
                altFormat: 'H:i',
                altInput: true,
                allowInput: true,
                noCalendar: true,
                enableTime: true,
                time_24hr: true,
                minTime: computedMinimumArrivalTime,
                minuteIncrement: 1
              }"
              class="!pr-0"
              @on-change="(...args) => onChangeArrivalHours(args)"
              @on-close="onCloseCalendar"
            />
          </div>
          <div class="w-3/12">
            <Label :required="false" label-text="Timezone:" class="whitespace-nowrap" />
            <SelectField
              :model-value="missionFormModel.legs[legIndex].arrival_datetime_is_local"
              :options="[
                { label: 'UTC', value: false },
                { label: 'Local', value: true }
              ]"
              :reduce="(item) => item.value"
              :clearable="false"
              :disabled="!missionFormModel.legs[legIndex].arrival_location?.is_lat_lon_available"
              label="label"
              placeholder="Timezone"
              class="timezone-select mb-0 re-css"
              :append-to-body="false"
              @update:model-value="onChangeTimeZone('arrival_datetime_is_local', $event)"
            />
          </div>
        </div>
      </div>
      <InputField
        v-model.uppercase="missionFormModel.legs[legIndex].callsign_override"
        :errors="errors?.callsign_override"
        :is-validation-dirty="isValidationDirty"
        label-text="Callsign (if different):"
        placeholder=""
      />
      <InputField
        :model-value="missionFormModel.legs[legIndex].pob_crew"
        required
        type="number"
        :is-validation-dirty="isValidationDirty"
        label-text="Crew:"
        placeholder="Please enter Crew"
        :errors="errors?.pob_crew"
        @update:model-value="onCrewUpdate"
      />
    </div>
  </div>
  <div class="flex mb-[18px]">
    <div class="flex px-[1.5rem] mt-[6px] gap-[1.5rem] w-full">
      <div class="flex w-1/2 flex-col">
        <div>
          <CheckboxField
            v-model="passengersCheckbox"
            label-text="Passengers?"
            @update:model-value="onHandleCheckBox($event, 'pob_pax')"
          />
          <InputField
            v-model="passengersQuantityComputed"
            placeholder=""
            type="number"
            :is-validation-dirty="isValidationDirty"
            :errors="errors?.pob_pax"
            :disabled="!passengersCheckbox"
          />
        </div>
      </div>
      <div class="flex w-1/2 flex-col">
        <div>
          <CheckboxField
            v-model="cargoCheckbox"
            label-text="Cargo? (lbs)"
            @update:model-value="onHandleCheckBox($event, 'cob_lbs')"
          />
          <InputField
            v-model="cargoQuantityComputed"
            placeholder=""
            type="number"
            :is-validation-dirty="isValidationDirty"
            :errors="errors?.cob_lbs"
            :disabled="!cargoCheckbox"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, createRenderer, PropType, watch } from 'vue'
import {
  Label,
  FlatPickr,
  InputField,
  CheckboxField,
  SelectField,
  AirportLocationApiSelectField
} from 'shared/components'
import { ErrorObject } from '@vuelidate/core'
import type { ILegService, IMissionLegFormStructure } from '@/types/mission/mission.types'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import { useMissionReferenceStore } from '@/stores/useMissionReferenceStore'
import { missionLegServiceDefaults } from '@/constants/mission.constants'
import { useMissionLegTime } from '@/composables/mission/mission-leg/useMissionLegTime'
import { useAirportLocation } from '@/composables/mission/mission-leg/useAirportLocation'
import { storeToRefs } from 'pinia'

const props = defineProps({
  legIndex: {
    type: Number,
    default: 0
  },
  isValidationDirty: {
    type: Boolean,
    default: false
  },
  errors: {
    type: Object as PropType<Record<string, ErrorObject[]>>,
    default: () => ({})
  }
})
const {
  dateTime,
  computedMinimumDepartureDate,
  computeMinimumArrivalDate,
  computedMinimumArrivalTime,
  computedMinimumDepartureTime,
  onCloseCalendar,
  onChangeDepartureDate,
  onChangeDepartureHours,
  onChangeArrivalDate,
  onChangeArrivalHours,
  onChangeTimeZone
} = useMissionLegTime(props.legIndex as number)

const { onChangeArrivalLocation, onChangeDepartureLocation } = useAirportLocation(
  props.legIndex as number
)

const missionFormStore = useMissionFormStore()
const missionsReferenceStore = useMissionReferenceStore()

const { selectedDestinationAirportsLeg, passengerService, cargoService } =
  storeToRefs(missionsReferenceStore)
const { formModel: missionFormModel } = storeToRefs(missionFormStore)

const passengersCheckbox = computed(() => {
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]

  return currentLeg?.arrival_aml_service || prevLeg?.arrival_aml_service
    ? isServiceSelected(passengerService.value?.id as number)
    : currentLeg?.pob_pax !== null
})

const passengersQuantityComputed = computed({
  get: () => missionFormModel.value?.legs?.[props.legIndex]?.pob_pax,
  set: (value: number) => {
    const leg = missionFormModel.value.legs[props.legIndex]
    if (+value < 0) return (leg.pob_pax = 0)
    leg.pob_pax = value
  }
})

const cargoCheckbox = computed(() => {
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
  return currentLeg?.cob_lbs !== null
})

const cargoQuantityComputed = computed<number>({
  get: () => missionFormModel.value?.legs?.[props.legIndex]?.cob_lbs as number,
  set: (value: number) => {
    const leg = missionFormModel.value.legs?.[props.legIndex]
    if (!leg) return
    if (+value < 0) return (leg.cob_lbs = 0)
    leg.cob_lbs = value
    onHandleLegServicing(true, cargoService?.value?.id)
  }
})

const isServiceSelected = (serviceId?: number): boolean => {
  if (!serviceId) return false
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]

  const isSelectedInPrevLeg = !!prevLeg?.servicing?.services?.find(
    (service) => service?.service === serviceId
  )?.on_departure
  const isSelectedInCurrentLeg = !!currentLeg?.servicing?.services?.find(
    (service) => service?.service === serviceId
  )?.on_arrival

  return isSelectedInPrevLeg || isSelectedInCurrentLeg
}

/** function handles leg Cargo & Passenger checkbox handling
 * @param flag - checkbox state
 * @param property - dependant on checkbox leg property
 * */
const onHandleCheckBox = (
  flag: boolean,
  property: keyof Pick<IMissionLegFormStructure, 'pob_pax' | 'cob_lbs'>
) => {
  const currLeg = missionFormModel.value?.legs?.[props.legIndex]
  currLeg && (currLeg[property] = flag ? 0 : null)
  if (property === 'pob_pax') {
    onHandleLegServicingPob(flag, passengerService.value?.id)
  } else {
    onHandleLegServicing(flag, cargoService.value?.id)
  }
}

/** function handles leg additional servicing dependant on passenger & cargo checkboxes
 * @param flag - checkbox state
 * @param service - dependant service id (passenger_handling / cargo_handling) get from reference store
 */
const onHandleLegServicing = (flag: boolean, service?: number) => {
  // Do not handle if service is missing
  if (!service) return
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
  const nextLeg = missionFormModel.value?.legs?.[props.legIndex + 1]
  const doubleLeg = missionFormModel.value?.legs?.[props.legIndex + 2]
  const handleService = (
    leg: IMissionLegFormStructure,
    servicingType: 'on_departure' | 'on_arrival'
  ) => {
    if (!leg.servicing?.services) return
    const serviceIndex = (leg?.servicing?.services as ILegService[])?.findIndex(
      (item) => item?.service === service
    )
    const prevserviceIndex = (prevLeg?.servicing?.services as ILegService[])?.findIndex(
      (item) => item?.service === service
    )
    const currentserviceIndex = (currentLeg?.servicing?.services as ILegService[])?.findIndex(
      (item) => item?.service === service
    )
    const specialCurrent = currentLeg?.servicing?.services?.map((item) => {
      if (item.service === service) {
        return item.service
      }
    })
    const specialPrev = prevLeg?.servicing?.services?.map((item) => {
      if (item.service === service) {
        return item.service
      }
    })
    const oppositeServicingType = servicingType === 'on_departure' ? 'on_arrival' : 'on_departure'

    const enable_service =
      prevLeg?.cob_lbs === null || currentLeg?.cob_lbs === null || nextLeg?.cob_lbs === null
        ? true
        : Number(prevLeg?.cob_lbs) !== Number(currentLeg?.cob_lbs) ||
          Number(currentLeg?.cob_lbs) !== Number(nextLeg?.cob_lbs)
    //Add service if it is not present
    // prevLeg value is exist and nextLeg value is exist and when currentLeg cargo selected, service state (review)
    if (
      flag &&
      doubleLeg?.cob_lbs === undefined &&
      Number(currentLeg?.cob_lbs) > 0 &&
      Number(nextLeg?.cob_lbs) > 0 &&
      prevserviceIndex > 0 &&
      Number(currentLeg?.cob_lbs) !== Number(nextLeg?.cob_lbs)
    ) {
      if (serviceIndex < 0) {
        currentLeg.servicing.services.push({
          ...missionLegServiceDefaults(service),
          [servicingType]: true,
          [oppositeServicingType]: true
        })
        return
      }
    }
    // when cargo checkbox disable, on_departure(prev), on_arrival(current)'s value true.
    if (
      (!flag || Number(currentLeg?.cob_lbs) === 0) &&
      serviceIndex < 0 &&
      Number(prevLeg?.cob_lbs) > 0 &&
      Number(nextLeg?.cob_lbs) > 0 &&
      Number(currentLeg?.cob_lbs) !== Number(prevLeg?.cob_lbs) &&
      Number(currentLeg?.cob_lbs) !== Number(nextLeg?.cob_lbs)
    ) {
      leg.servicing.services.push({
        ...missionLegServiceDefaults(service),
        [oppositeServicingType]: true
      })
      return
    }

    if (
      flag &&
      serviceIndex < 0 &&
      Number(prevLeg?.cob_lbs) > 0 &&
      Number(nextLeg?.cob_lbs) > 0 &&
      Number(currentLeg?.cob_lbs) !== Number(prevLeg?.cob_lbs) &&
      Number(currentLeg?.cob_lbs) !== Number(nextLeg?.cob_lbs)
    ) {
      leg.servicing.services.push({
        ...missionLegServiceDefaults(service),
        [oppositeServicingType]: true,
        [servicingType]: true
      })
      return
    }

    if (
      serviceIndex < 0 &&
      Number(currentLeg?.cob_lbs) > 0 &&
      Number(prevLeg?.cob_lbs) > 0 &&
      Number(nextLeg?.cob_lbs) > 0 &&
      Number(currentLeg?.cob_lbs) !== Number(prevLeg?.cob_lbs) &&
      Number(currentLeg?.cob_lbs) !== Number(nextLeg?.cob_lbs)
    ) {
      flag &&
        leg.servicing.services.push({
          ...missionLegServiceDefaults(service),
          [servicingType]: true,
          [oppositeServicingType]: true
        })
      return
    }
    if (
      prevLeg?.cob_lbs !== undefined &&
      prevserviceIndex < 0 &&
      Number(nextLeg?.cob_lbs) === Number(currentLeg?.cob_lbs) &&
      Number(prevLeg?.cob_lbs) !== Number(currentLeg?.cob_lbs) &&
      flag &&
      Number(prevLeg?.cob_lbs) > 0 &&
      serviceIndex < 0
    ) {
      prevLeg.servicing.services.push({
        ...missionLegServiceDefaults(service),
        [servicingType]: true,
        [oppositeServicingType]: true
      })
      return
    }
    // first current cargo disabled, on_departure === true
    if (
      (!flag || Number(currentLeg?.cob_lbs) === 0) &&
      serviceIndex < 0 &&
      currentserviceIndex < 0 &&
      (Number(prevLeg?.cob_lbs) === 0 || prevLeg?.cob_lbs === undefined) &&
      Number(currentLeg?.cob_lbs) === 0 &&
      Number(nextLeg?.cob_lbs) > 0
    ) {
      currentLeg.servicing.services.push({
        ...missionLegServiceDefaults(service),
        [oppositeServicingType]: true
      })
      return
    }
    // Should we even consider the nextLeg = undefined?
    if (
      (!flag || Number(currentLeg?.cob_lbs) === 0) &&
      serviceIndex < 0 &&
      prevserviceIndex < 0 &&
      Number(currentLeg?.cob_lbs) === 0 &&
      Number(prevLeg?.cob_lbs) > 0 &&
      //(Number(nextLeg?.cob_lbs) === 0 || nextLeg?.cob_lbs === undefined)
      !nextLeg?.cob_lbs
    ) {
      prevLeg?.servicing.services.push({
        ...missionLegServiceDefaults(service),
        [oppositeServicingType]: true
      })
      return
    }

    if (
      flag &&
      serviceIndex < 0 &&
      prevserviceIndex < 0 &&
      Number(currentLeg?.cob_lbs) > 0 &&
      Number(prevLeg?.cob_lbs) > 0 &&
      nextLeg?.cob_lbs === undefined &&
      Number(currentLeg?.cob_lbs) !== Number(prevLeg?.cob_lbs)
    ) {
      prevLeg?.servicing?.services?.push({
        ...missionLegServiceDefaults(service),
        [oppositeServicingType]: true,
        [servicingType]: true
      })
      return
    }

    if (
      flag &&
      serviceIndex < 0 &&
      prevserviceIndex < 0 &&
      Number(prevLeg?.cob_lbs) === 0 &&
      Number(nextLeg?.cob_lbs) > 0 &&
      Number(currentLeg?.cob_lbs) > 0 &&
      Number(nextLeg?.cob_lbs) === Number(currentLeg?.cob_lbs)
    ) {
      prevLeg?.servicing?.services?.push({
        ...missionLegServiceDefaults(service),
        [servicingType]: true
      })
      return
    }

    // Remove service if not used

    // when current cargo value equal prevLeg value and nextLeg value delete event
    if (
      flag &&
      Number(prevLeg?.cob_lbs) > 0 &&
      Number(currentLeg?.cob_lbs) > 0 &&
      Number(nextLeg?.cob_lbs) > 0 &&
      Number(prevLeg?.cob_lbs) === Number(currentLeg?.cob_lbs) &&
      Number(nextLeg?.cob_lbs) === Number(currentLeg?.cob_lbs)
    ) {
      if (serviceIndex < 0) return
      return leg.servicing.services.splice(serviceIndex, 1)
    } else if (
      leg.servicing.services?.[serviceIndex]?.[oppositeServicingType] !== null &&
      Number(nextLeg?.cob_lbs) === Number(currentLeg?.cob_lbs) &&
      Number(prevLeg?.cob_lbs) !== Number(currentLeg?.cob_lbs) &&
      flag &&
      Number(nextLeg?.cob_lbs) > 0 &&
      specialCurrent?.[serviceIndex] === service
    ) {
      if (serviceIndex < 0) return
      return currentLeg?.servicing?.services?.splice(serviceIndex, 1)
    } else {
      /* empty */
    }

    if (
      !leg.servicing.services?.[serviceIndex]?.[oppositeServicingType] &&
      (!flag || Number(currentLeg?.cob_lbs) === 0 || !enable_service)
    ) {
      if (serviceIndex < 0) return
      return leg.servicing.services.splice(serviceIndex, 1)
    }

    if (
      flag &&
      currentserviceIndex < 0 &&
      Number(currentLeg?.cob_lbs) > 0 &&
      Number(nextLeg?.cob_lbs) > 0 &&
      Number(prevLeg?.cob_lbs) === Number(currentLeg?.cob_lbs) &&
      Number(currentLeg?.cob_lbs) !== Number(nextLeg?.cob_lbs)
    ) {
      if (serviceIndex < 0) {
        currentLeg?.servicing?.services?.push({
          ...missionLegServiceDefaults(service),
          [servicingType]: true,
          [oppositeServicingType]: true
        })
        return
      }
    }

    if (
      flag &&
      leg.servicing.services?.[serviceIndex]?.[oppositeServicingType] !== null &&
      currentserviceIndex < 0 &&
      Number(prevLeg?.cob_lbs) > 0 &&
      Number(currentLeg?.cob_lbs) > 0 &&
      Number(prevLeg?.cob_lbs) === Number(currentLeg?.cob_lbs) &&
      Number(nextLeg?.cob_lbs) === 0
    ) {
      currentLeg.servicing.services.push({
        ...missionLegServiceDefaults(service),
        [oppositeServicingType]: true
      })
      return
    }

    if (
      leg.servicing.services?.[serviceIndex]?.[oppositeServicingType] !== null &&
      specialPrev?.[serviceIndex] === service &&
      Number(prevLeg?.cob_lbs) > 0 &&
      Number(currentLeg?.cob_lbs) > 0 &&
      ((Number(prevLeg?.cob_lbs) === Number(currentLeg?.cob_lbs) &&
        (Number(nextLeg?.cob_lbs) === 0 || nextLeg?.cob_lbs === undefined)) ||
        Number(prevLeg?.cob_lbs) === Number(currentLeg?.cob_lbs))
    ) {
      if (serviceIndex < 0) return
      return prevLeg?.servicing?.services?.splice(serviceIndex, 1)
    }
    //nextLeg is exist and when current checkbox click (review)
    if (
      flag &&
      serviceIndex < 0 &&
      currentserviceIndex < 0 &&
      Number(currentLeg?.cob_lbs) > 0 &&
      Number(nextLeg?.cob_lbs) > 0 &&
      Number(currentLeg?.cob_lbs) !== Number(nextLeg?.cob_lbs)
    ) {
      currentLeg.servicing.services.push({
        ...missionLegServiceDefaults(service),
        [servicingType]: true,
        [oppositeServicingType]: true
      })
      return
    }

    if (
      flag &&
      serviceIndex < 0 &&
      prevserviceIndex < 0 &&
      Number(prevLeg?.cob_lbs) > 0 &&
      Number(currentLeg?.cob_lbs) &&
      Number(nextLeg?.cob_lbs) === 0 &&
      Number(prevLeg?.cob_lbs) !== Number(currentLeg?.cob_lbs) &&
      Number(currentLeg?.cob_lbs) !== Number(nextLeg?.cob_lbs)
    ) {
      prevLeg?.servicing?.services?.push({
        ...missionLegServiceDefaults(service),
        [servicingType]: true,
        [oppositeServicingType]: true
      })
      return
    }
    if (
      flag &&
      Number(prevLeg?.cob_lbs) > 0 &&
      Number(currentLeg?.cob_lbs) > 0 &&
      Number(nextLeg?.cob_lbs > 0) &&
      Number(prevLeg?.cob_lbs) !== Number(currentLeg?.cob_lbs) &&
      Number(currentLeg?.cob_lbs) === Number(nextLeg?.cob_lbs)
    ) {
      if (serviceIndex < 0) return
      return currentLeg?.servicing?.services?.splice(serviceIndex, 1)
    }

    if (serviceIndex < 0 && Number(currentLeg?.cob_lbs) > 0) {
      //default
      flag &&
        enable_service &&
        leg.servicing.services.push({
          ...missionLegServiceDefaults(service),
          [servicingType]: true
        })
      return
    }

    if (currentLeg?.cob_lbs !== null && Number(currentLeg?.cob_lbs) === 0) {
      return (leg.servicing.services[serviceIndex] = {
        ...(leg.servicing.services[serviceIndex] as ILegService),
        [servicingType]: false
      })
    }
    return (leg.servicing.services[serviceIndex] = {
      ...(leg.servicing.services[serviceIndex] as ILegService),
      [servicingType]: flag && enable_service
    })
  }

  if (prevLeg?.arrival_aml_service && prevLeg?.servicing && prevLeg?.servicing?.services) {
    handleService(prevLeg, 'on_departure')
  }
  if (currentLeg?.arrival_aml_service && currentLeg?.servicing && currentLeg?.servicing?.services) {
    handleService(currentLeg, 'on_arrival')
  }
}

const onHandleLegServicingPob = (flag: boolean, service?: number) => {
  // Do not handle if service is missing
  if (!service) return
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
  const handleService = (
    leg: IMissionLegFormStructure,
    servicingType: 'on_departure' | 'on_arrival'
  ) => {
    if (!leg.servicing?.services) return
    const serviceIndex = (leg?.servicing?.services as ILegService[])?.findIndex(
      (item) => item?.service === service
    )
    const oppositeServicingType = servicingType === 'on_departure' ? 'on_arrival' : 'on_departure'
    // Add service if it is not present
    if (serviceIndex < 0) {
      flag &&
        leg.servicing.services.push({
          ...missionLegServiceDefaults(service),
          [servicingType]: true
        })
      return
    }
    // Remove service if not used
    if (!leg.servicing.services?.[serviceIndex]?.[oppositeServicingType] && !flag) {
      if (serviceIndex < 0) return
      return leg.servicing.services.splice(serviceIndex, 1)
    }
    // Update service flag
    return (leg.servicing.services[serviceIndex] = {
      ...(leg.servicing.services[serviceIndex] as ILegService),
      [servicingType]: flag
    })
  }
  if (prevLeg?.arrival_aml_service && prevLeg?.servicing && prevLeg?.servicing?.services) {
    handleService(prevLeg, 'on_departure')
  }
  if (currentLeg?.arrival_aml_service && currentLeg?.servicing && currentLeg?.servicing?.services) {
    handleService(currentLeg, 'on_arrival')
  }
}

/** function adds automatical services based on cargo & passenger checkboxes
 */
const handleAutomaticalServices = () => {
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
  const nextLeg = missionFormModel.value?.legs?.[props.legIndex + 1]

  const addOrUpdateService = (
    serviceId: number | undefined,
    servicingType: 'on_departure' | 'on_arrival'
  ) => {
    if (!currentLeg.servicing?.services) return

    const serviceIndex = (currentLeg?.servicing?.services as ILegService[])?.findIndex(
      (item) => item?.service === serviceId
    )
    serviceIndex > -1
      ? (currentLeg.servicing.services[serviceIndex] = {
          ...currentLeg.servicing.services[serviceIndex],
          [servicingType]: true
        } as ILegService)
      : currentLeg.servicing?.services?.push({
          ...missionLegServiceDefaults(serviceId as number),
          [servicingType]: true
        })
  }
  if (currentLeg?.cob_lbs !== null) {
    addOrUpdateService(cargoService.value?.id, 'on_arrival')
  }
  if (currentLeg?.pob_pax !== null) {
    addOrUpdateService(passengerService.value?.id, 'on_arrival')
  }
  if (nextLeg?.cob_lbs !== null) {
    addOrUpdateService(cargoService.value?.id, 'on_departure')
  }
  if (nextLeg?.pob_pax !== null) {
    addOrUpdateService(passengerService.value?.id, 'on_departure')
  }
}

const onCrewUpdate = (value) => {
  missionFormModel.value.legs[props.legIndex].pob_crew = value

  if (missionFormModel.value.legs.length) {
    missionFormModel.value.legs = missionFormModel.value.legs.map((el, index) =>
      index <= props.legIndex ? el : { ...el, pob_crew: value }
    )
  }
}

watch(passengersCheckbox, (flag) => {
  const currLeg = missionFormModel.value?.legs?.[props.legIndex]
  if (!flag) currLeg?.pob_pax === null && (currLeg.pob_pax = null)
  else if (flag && missionFormModel.value.legs?.[props.legIndex]?.pob_pax === null) currLeg!.pob_pax = 0
})

watch(cargoCheckbox, (flag) => {
  const currLeg = missionFormModel.value?.legs?.[props.legIndex]
  if (!flag) currLeg.cob_lbs = null
  else if (flag && missionFormModel.value.legs[props.legIndex]?.cob_lbs === null)
    currLeg.cob_lbs = 0
})

watch(
  () => missionFormModel.value?.legs?.[props.legIndex]?.arrival_aml_service,
  (isAmlServiceSelected) => {
    if (isAmlServiceSelected) {
      handleAutomaticalServices()
    }
  }
)

watch(
  () => missionFormModel.value.legs[props.legIndex]?.arrival_location,
  (location) => {
    if (location?.id) selectedDestinationAirportsLeg.value[props.legIndex] = location
  }
)
</script>

<style lang="scss" module>
.mission-leg-wrapper {
  @apply relative flex flex-col bg-white min-w-0 rounded-[0.5rem];

  &__content {
    @apply grid px-6 gap-x-[1.5rem] gap-y-[2.5px] mt-4  grid-cols-1 lg:grid-cols-2 font-medium text-[1.25rem] text-grey-900;
  }
}
</style>
<style lang="scss">
.timezone-select {
  .vs__dropdown-menu {
    @apply min-w-[5rem] #{!important};
  }
}
.re-css {
  div > div > div > span.vs__selected {
    overflow: visible !important;
  }
}
</style>
