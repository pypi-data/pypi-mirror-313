import { computed, nextTick, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import dayjs from 'dayjs'
import type { IMissionLeg } from '@/types/mission/mission.types'
import { getMissionId } from '@/helpers'
import { useMissionStore } from '@/stores/useMissionStore'

export const useMissionLegTime = (legIndex: number) => {
  const { formModel: missionFormModel } = storeToRefs(useMissionFormStore())
  const { isFetchingMission, mission } = storeToRefs(useMissionStore())

  const isInitMission = ref(false)
  const DEFAULT_TIME = '12:00'

  const dateTime = ref<Record<string, string>>({
    departureDate: missionFormModel.value?.legs[legIndex]?.departure_datetime ?? '',
    departureTime: missionFormModel.value?.legs[legIndex]?.departure_datetime
      ? dayjs(missionFormModel.value?.legs[legIndex]?.departure_datetime).format('HH:mm')
      : '',
    arrivalDate: missionFormModel.value?.legs[legIndex]?.arrival_datetime ?? '',
    arrivalTime: missionFormModel.value?.legs[legIndex]?.arrival_datetime
      ? dayjs(missionFormModel.value?.legs[legIndex]?.arrival_datetime).format('HH:mm')
      : ''
  })

  // commented for now - start time for departure date
  const startDepartureTime = computed(() => {
    const prevLeg = missionFormModel.value.legs?.[legIndex - 1]
    const [hours, minutes] = [
      new Date(prevLeg?.arrival_datetime as string).getHours(),
      new Date(prevLeg?.arrival_datetime as string).getMinutes()
    ]
    return prevLeg?.arrival_datetime ? { hours, minutes } : null
  })

  // commented for now - start time for arrival date
  const startArrivalTime = computed(() => {
    const departureDateTime = missionFormModel.value.legs?.[legIndex]?.departure_datetime

    if (!departureDateTime) return null

    const [hours, minutes] = [
      new Date(departureDateTime).getHours(),
      new Date(departureDateTime).getMinutes()
    ]

    return { hours, minutes }
  })
  const computedMinimumDepartureDate = computed(() => {
    return legIndex === 0
      ? null
      : new Date(
          new Date(missionFormModel.value?.legs?.[legIndex - 1]?.arrival_datetime).setHours(
            0,
            0,
            0,
            0
          )
        )
  })

  const computeMinimumArrivalDate = computed(
    () =>
      new Date(
        new Date(missionFormModel.value?.legs[legIndex]?.departure_datetime).setHours(0, 0, 0, 0)
      )
  )

  const computedMinimumDepartureTime = computed(() => {
    const getLeg = (index: number) => missionFormModel.value?.legs?.[index]
    const legDepartureTime = getLeg(legIndex)?.departure_datetime as string
    const legArrivalTime = getLeg(legIndex - 1)?.arrival_datetime as string

    const departureDate = new Date(legDepartureTime).setHours(0, 0, 0, 0)
    const arrivalDate = new Date(legArrivalTime).setHours(0, 0, 0, 0)

    const [hours, minutes] = [
      new Date(legArrivalTime)?.getHours(),
      new Date(legArrivalTime)?.getMinutes() + 1
    ]
    const h = !isNaN(hours) ? String(hours).padStart(2, '0') : '00'
    const m = !isNaN(minutes) ? String(minutes).padStart(2, '0') : '00'
    return legIndex === 0 || departureDate !== arrivalDate ? null : `${h}:${m}`
  })

  const computedMinimumArrivalTime = computed(() => {
    const getLeg = (index: number) => missionFormModel.value?.legs?.[index]
    const legDepartureTime = getLeg(legIndex)?.departure_datetime as string
    const legArrivalTime = getLeg(legIndex)?.arrival_datetime as string

    if (!legDepartureTime) return null

    const departureDate = new Date(legDepartureTime).setHours(0, 0, 0, 0)
    const arrivalDate = new Date(legArrivalTime).setHours(0, 0, 0, 0)

    const [hours, minutes] = [
      new Date(legDepartureTime).getHours(),
      new Date(legDepartureTime).getMinutes() + 1
    ]
    const h = !isNaN(hours) ? String(hours).padStart(2, '0') : '00'
    const m = !isNaN(minutes) ? String(minutes).padStart(2, '0') : '00'
    return departureDate !== arrivalDate ? null : `${h}:${m}`
  })

  const addMinutes = (date: Date, minutes: number) => date.setMinutes(date.getMinutes() + minutes)
  const addHours = (date: Date, hours: number) => date.setHours(date.getHours() + hours)
  const onChangeDepartureDate = async (event: any) => {
    await nextTick()
    const currentLeg = missionFormModel.value?.legs?.[legIndex]
    const [dates] = event
    const time = dateTime.value.departureTime?.split(':').map((el) => Number(el))
    if (!dates[0] || !currentLeg) return

    //check if date is already selected
    if (dateTime.value.departureTime) {
      currentLeg.departure_datetime = new Date(dates[0].setHours(...time)) as unknown as string
    } else {
      currentLeg.departure_datetime = dates[0]
      dateTime.value.departureTime = DEFAULT_TIME
    }
    // check if departure date is bigger then the arrival date
    if (dates[0] && new Date(dates[0]) >= new Date(currentLeg.arrival_datetime as string)) {
      // add +1 minute to time
      currentLeg.arrival_datetime = dayjs(addHours(new Date(dates[0]), 1)).$d
      dateTime.value.arrivalDate = dates[0]
      dateTime.value.arrivalTime = dayjs(addHours(new Date(dates[0]), 1)).format('HH:mm')
    }
  }
  const onChangeDepartureHours = (event: any) => {
    const currentLeg = missionFormModel.value?.legs?.[legIndex]
    const [dates, timeStr] = event
    if (!timeStr || isInitMission.value || !currentLeg) return
    const time = timeStr.split(':').map((el: string) => Number(el))

    //check if date is already selected
    if (currentLeg.departure_datetime) {
      currentLeg.departure_datetime = new Date(
        currentLeg.departure_datetime.setHours(...time)
      ) as unknown as string
    } else {
      currentLeg.departure_datetime = dates[0]
      dateTime.value.departureDate = new Date(dates[0]) as unknown as string
    }

    // check if departure date is bigger then the arrival date
    if (
      currentLeg.departure_datetime &&
      new Date(currentLeg.departure_datetime) >= new Date(currentLeg.arrival_datetime as string)
    ) {
      const arrDate: Date = new Date(currentLeg.departure_datetime.setHours(...time))
      currentLeg.arrival_datetime = dayjs(addHours(arrDate, 1)).$d
      dateTime.value.arrivalDate = new Date(arrDate) as unknown as string

      // add +1 minute to time
      dateTime.value.arrivalTime = dayjs(
        addHours(new Date(currentLeg.departure_datetime), 1)
      ).format('HH:mm')
    }
  }
  const onChangeArrivalDate = async (event: any) => {
    await nextTick()
    const currentLeg = missionFormModel.value?.legs?.[legIndex]
    const [dates] = event
    if (!dates[0] || !currentLeg) return
    const time = dateTime.value.arrivalTime?.split(':').map((el) => Number(el))
    if (dateTime.value.arrivalTime) {
      currentLeg.arrival_datetime = new Date(dates[0].setHours(...time)) as unknown as string
    } else {
      currentLeg.arrival_datetime = dates[0]
      dateTime.value.arrivalTime = DEFAULT_TIME
    }
  }
  const onChangeArrivalHours = (event: any) => {
    const currentLeg = missionFormModel.value?.legs?.[legIndex]
    const [dates, timeStr] = event
    if (!timeStr || isInitMission.value || !currentLeg) return
    const time = timeStr.split(':').map((el: string) => Number(el))
    if (currentLeg.arrival_datetime) {
      currentLeg.arrival_datetime = new Date(
        currentLeg.arrival_datetime?.setHours(...time)
      ) as unknown as string
    } else {
      currentLeg.arrival_datetime = dates[0]
      dateTime.value.arrivalDate = dates[0]
    }
  }
  const onChangeTimeZone = (field: string, event: boolean) => {
    const currentLeg = missionFormModel.value?.legs?.[legIndex]
    if (!currentLeg) return
    currentLeg.departure_datetime_is_local = event
    currentLeg.arrival_datetime_is_local = event
  }
  const fillDateLeg = (legInfo: IMissionLeg) => {
    isInitMission.value = true

    dateTime.value = {
      departureDate: legInfo.departure_datetime,
      departureTime: dayjs(legInfo.departure_datetime).format('HH:mm'),
      arrivalDate: legInfo.arrival_datetime,
      arrivalTime: dayjs(legInfo.arrival_datetime).format('HH:mm')
    }
  }
  const onCloseCalendar = (date: Array<Date>, value: string, instance: Record<string, any>) => {
    value && instance.setDate(value, true)
  }

  watch(
    () => missionFormModel.value?.legs[legIndex - 1]?.arrival_datetime,
    (date) => {
      const currentLeg = missionFormModel.value?.legs?.[legIndex]
      if (!currentLeg || !date) return
      const currentDepartureDate = new Date(currentLeg?.departure_datetime || 0).getTime()
      const prevArrivalDate = new Date(date).getTime()
      if (date && currentDepartureDate <= prevArrivalDate) {
        currentLeg.departure_datetime = dayjs(addHours(new Date(date), 1)).$d
        dateTime.value.departureDate = currentLeg.departure_datetime as string
        dateTime.value.departureTime = dayjs(addHours(new Date(date), 1)).format('HH:mm')
      }
    }
  )
  watch(
    () => isFetchingMission.value,
    () => {
      getMissionId() &&
        !isFetchingMission.value &&
        queueMicrotask(() => fillDateLeg(mission.value?.legs[legIndex] as unknown as IMissionLeg))
      queueMicrotask(() => (isInitMission.value = false))
    },
    { deep: true }
  )
  return {
    dateTime,
    computedMinimumDepartureDate,
    computeMinimumArrivalDate,
    computedMinimumArrivalTime,
    computedMinimumDepartureTime,
    addMinutes,
    onCloseCalendar,
    onChangeDepartureDate,
    onChangeDepartureHours,
    onChangeArrivalDate,
    onChangeArrivalHours,
    onChangeTimeZone
  }
}
