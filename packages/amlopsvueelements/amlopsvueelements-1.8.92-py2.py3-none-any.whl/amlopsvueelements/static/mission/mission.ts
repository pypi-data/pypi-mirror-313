import type {
  IExtendedMission,
  IMission,
  IMissionFormStructure,
  IMissionLeg
} from '@/types/mission/mission.types'
import type { Nullable } from '@/types/generic.types'
import type {
  ITurnarounds,
  ITurnaroundService
} from '@/types/mission-turnarounds/mission-turnarounds'
import { turnaroundNonEditableServices } from '@/constants/service.constants'
import type { IService } from '@/types/mission/mission-reference.types'
import dayjs from 'dayjs'

export const mapExtendedMission = (mission: IExtendedMission): IMissionFormStructure => {
  const mappedLegs = mission.legs.map((leg) => ({
    ...leg,
    departure_location: {
      id: leg?.departure_location?.id,
      full_repr: leg?.departure_location?.full_repr,
      tiny_repr: leg?.arrival_location?.tiny_repr,
      is_lat_lon_available: leg?.departure_location?.is_lat_lon_available
    },
    arrival_location: {
      id: leg?.arrival_location?.id,
      full_repr: leg?.arrival_location?.full_repr,
      tiny_repr: leg?.arrival_location?.tiny_repr,
      is_lat_lon_available: leg?.arrival_location?.is_lat_lon_available
    },
    servicing: leg?.servicing
      ? {
          ...leg?.servicing,
          fuel_unit: leg?.servicing?.fuel_unit?.id ?? null,
          services: leg?.servicing?.services?.map((service) => {
            return {
              ...service,
              service: service?.service?.id,
              quantity_selection_uom: service?.service?.quantity_selection_uom,
              is_allowed_free_text: service?.service?.is_allowed_free_text,
              is_allowed_quantity_selection: service?.service?.is_allowed_quantity_selection
            }
          })
        }
      : undefined
  }))
  return {
    ...mission,
    type: mission?.type?.id,
    organisation: { id: mission?.organisation?.id, full_repr: mission?.organisation?.full_repr },
    requesting_person: mission?.requesting_person?.id,
    aircraft_type: mission?.aircraft_type?.id,
    aircraft: mission?.aircraft?.id,
    mission_planner: mission?.mission_planner?.id,
    legs: mappedLegs
  }
}

export const mapFormMission = (mission: Nullable<IMissionFormStructure>): Nullable<IMission> => {
  const missionLegs: { arrival_location: number | null; departure_location: number | null }[] =
    mission.legs?.map((leg) => ({
      ...leg,
      departure_location: leg?.departure_location?.id ?? null,
      arrival_location: leg?.arrival_location?.id ?? null
    })) ?? []
  return {
    ...mission,
    organisation: mission.organisation?.id ?? null,
    legs: missionLegs as Nullable<IMissionLeg>[]
  }
}

export const mapExtendedTurnarounds = (turnarounds: ITurnarounds[]): any => {
  return turnarounds.map((turnaround: ITurnarounds) => ({
    ...turnaround,
    services: turnaround.services?.map((service: ITurnaroundService) => {
      return {
        ...service,
        service: `${service.service.id}`,
        quantity_selection_uom: service.service.quantity_selection_uom,
        is_allowed_free_text: service.service.is_allowed_free_text,
        is_allowed_quantity_selection: service.service.is_allowed_quantity_selection
      }
    })
  }))
}

export const isDisabledService = (serviceId: number, options: IService[]) =>
  turnaroundNonEditableServices.some(
    (serviceCode) => serviceCode === findServiceById(serviceId, options).code
  )

export const findServiceById = (id: number, options: IService[], airport?: number): any => {
  const res = options?.find((option: IService) => option.id === id)
  const availability = res?.attributes?.availability_bool?.find((item) => item.airport === airport)
  return {
    arrival: true,
    departure: true,
    name: res?.attributes?.name || 'Unknown',
    code: res?.attributes?.codename || 'Unknown',
    ...(res?.attributes?.is_dla
      ? {
          arrival: res?.attributes?.is_dla_visible_arrival,
          departure: res?.attributes?.is_dla_visible_departure
        }
      : res?.attributes?.availability_bool && res?.attributes?.availability_bool.length > 0
      ? availability
        ? { arrival: availability.arrival, departure: availability.departure }
        : {
            arrival: false,
            departure: false
          }
      : {})
  }
}
