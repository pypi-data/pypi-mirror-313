import { defineStore, storeToRefs } from 'pinia'
import { computed, reactive, ref, watch } from 'vue'
import {
  missionDefaultFormModel,
  missionLegDefaults,
  missionLegServicingDefaults
} from '@/constants/mission.constants'
import type { IMissionFormStructure, IMissionLegFormStructure } from '@/types/mission/mission.types'
import type { Nullable } from '@/types/generic.types'
import { useMissionStore } from '@/stores/useMissionStore'
import { mapExtendedMission } from '@/helpers/mission'
import { useMissionReferenceStore } from '@/stores/useMissionReferenceStore'

export const useMissionFormStore = defineStore('MissionForm', () => {
  const missionStore = useMissionStore()
  const missionReferenceStore = useMissionReferenceStore()
  const { quantityUnits } = storeToRefs(missionReferenceStore)
  const { mission } = storeToRefs(missionStore)

  const formModel = reactive<Nullable<IMissionFormStructure>>(missionDefaultFormModel())
  const formErrors = ref([])
  const windowWidth = ref(window.innerWidth)

  // Assigns updated or fetched mission data to form model
  watch(
    () => mission.value,
    (newMission) => {
      if (!newMission) return
      Object.assign(formModel, mapExtendedMission(newMission))
    }
  )
  watch(
    () => quantityUnits.value,
    () => {
      const quantityUnit = quantityUnits.value?.find((unit) => unit.description.includes('Pound'))
      formModel?.legs?.[0]?.servicing &&
        (formModel.legs[0].servicing.fuel_unit = quantityUnit?.id || null)
    }
  )

  const findMissionLeg = (sequenceId: number): Nullable<IMissionLegFormStructure> => {
    return (
      formModel.legs?.find((leg) => leg!.sequence_id === sequenceId) ||
      missionLegDefaults(sequenceId)
    )
  }

  const addNewMissionLeg = (sequenceId: number) => {
    if (!formModel.legs?.length) return
    const prevLeg = findMissionLeg(sequenceId)

    // Increment sequence_id for all the next legs after the inserted one
    formModel.legs.forEach((leg) => {
      if (leg?.sequence_id && leg.sequence_id > sequenceId) {
        leg.sequence_id++
      }
    })
    // Insert new forms, which arrival_location is the destination of the previous forms
    const newLegSequenceId = sequenceId + 1
    const newLegData: Nullable<IMissionLegFormStructure> = {
      ...missionLegDefaults(newLegSequenceId),
      departure_location: prevLeg.arrival_location,
      pob_crew: prevLeg?.pob_crew || 0,

      // set departure date and arrival date to new leg as arrival date from prev + 1 hour
      ...(prevLeg?.arrival_datetime
        ? {
            departure_datetime: new Date(
              new Date(prevLeg.arrival_datetime).getTime() + 60 * 60 * 1000
            ),
            arrival_datetime: new Date(
              new Date(prevLeg.arrival_datetime).getTime() + 2 * 60 * 60 * 1000
            )
          }
        : {})
    }
    // If user pick the last leg, insert the new leg before the last leg
    const isLastPicked = sequenceId === formModel.legs.length
    formModel.legs.splice(sequenceId, 0, newLegData)

    if (isLastPicked) {
      prevLeg.servicing = missionLegServicingDefaults()
      prevLeg.arrival_aml_service = true

      const nextLeg = findMissionLeg(sequenceId + 1)
      nextLeg.arrival_aml_service = false
      delete nextLeg.servicing
    }

    const isLastLeg = newLegSequenceId === formModel.legs.length
    const deleteServicingIndex: number = isLastLeg ? sequenceId - 1 : sequenceId
    const leg = formModel.legs[deleteServicingIndex]
    if (!leg) return
  }

  const deleteMissionLeg = (sequenceId: number) => {
    if (!formModel.legs?.length) return
    // const prevLeg = findMissionLeg(sequenceId - 1)
    // const nextLeg = findMissionLeg(sequenceId + 1)
    // nextLeg.arrival_location = prevLeg.departure_location

    // Update the arrival location and sequence Id of the next forms
    formModel.legs.forEach((leg) => {
      if (leg?.sequence_id && leg.sequence_id > sequenceId) {
        leg.sequence_id--
      }
    })
    // Remove forms
    const indexToRemove = formModel?.legs?.findIndex((leg) => leg?.sequence_id === sequenceId)
    if (indexToRemove && indexToRemove !== -1) {
      formModel.legs?.splice(indexToRemove, 1)
    }
  }

  return { formModel, findMissionLeg, addNewMissionLeg, deleteMissionLeg, formErrors, windowWidth }
})
