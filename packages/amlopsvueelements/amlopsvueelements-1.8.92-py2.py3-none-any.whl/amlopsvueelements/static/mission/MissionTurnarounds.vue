<template>
  <div id="mission-turnarounds" :class="$style['mission-turnarounds']">
    <div :class="$style['mission-turnarounds__table-wrapper']">
      <div ref="tableWrapperRef">
        <table
          class="relative"
          :class="[$style['mission-turnarounds__table'], $style['service-table']]"
        >
          <thead class="sticky top-0 left-0 z-[100]" :class="$style['service-table__header']">
            <tr>
              <th
                :class="[$style['mission-turnarounds__title'], $style['service-table__header-row']]"
                colspan="100%"
              >
                MISSION TURNAROUNDS
              </th>
            </tr>
            <tr :class="$style['service-table__header-row']">
              <th class="!p-2">FLIGHT LEGS</th>
              <th v-for="(item, index) in groundServicingLength" :key="index" class="!text-start">
                {{ item }}
              </th>
              <th></th>
            </tr>
            <tr :class="$style['service-table__header-row']">
              <th class="!p-2">SERVICE</th>
              <th v-for="item in groundServicing" :key="item.id">
                {{ item.location.tiny_repr }}
              </th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <template v-for="turnaround in turnaroundsModel" :key="turnaround.id">
              <tr v-if="!turnaround.is_deleted" :class="$style['service-table__body-row']">
                <td>
                  <div class="w-full relative">
                    <MissionTurnaroundsServiceSelect
                      v-model="turnaround.id"
                      :loading="isLoadingServices"
                      :disabled="isServiceSelectDisabled(turnaround.id)"
                      :clearable="!isServiceSelectDisabled(turnaround.id)"
                      :options="
                        filterServiceOptions(turnaround.id, turnaroundsModel, serviceOptions)
                      "
                      @search="onSearchService"
                    />
                    <div
                      v-if="turnaround.services?.length && !searchServiceQuery"
                      class="pointer-events-none absolute text-base top-2.5 text-[#a2aeb8] left-4"
                    >
                      Select service
                    </div>
                  </div>
                </td>
                <td
                  v-for="(service, index) of turnaround.turnarounds"
                  :key="index"
                  class="relative"
                  :class="[index !== 0 ? 'align-top' : '']"
                >
                  <div
                    v-if="!groundServicing[index]?.is_servicing_requested"
                    class="w-full h-full bg-grey-50/50 cursor-not-allowed absolute left-0 top-0 z-[100]"
                  />
                  <div>
                    <div class="flex gap-x-3 justify-center">
                      <div class="flex flex-col items-center">
                        <span>A</span>
                        <CheckboxField
                          v-model="service.on_arrival"
                          :disabled="
                            isDisabledService(turnaround.id, serviceOptions) ||
                            !findServiceById(
                              turnaround.id,
                              serviceOptions,
                              groundServicing[index]?.location.id
                            ).arrival
                          "
                          class="!mb-0 d-flex shrink-0"
                          size="24px"
                        />
                      </div>
                      <div class="flex flex-col items-center">
                        <span>D</span>
                        <CheckboxField
                          v-model="service.on_departure"
                          :disabled="
                            isDisabledService(turnaround.id, serviceOptions) ||
                            !findServiceById(
                              turnaround.id,
                              serviceOptions,
                              groundServicing[index]?.location.id
                            ).departure
                          "
                          class="!mb-0 d-flex shrink-0"
                          size="24px"
                        />
                      </div>
                    </div>
                    <div class="flex flex-col !gap-x-2 !gap-y-[0.5rem] mt-2">
                      <div
                        v-if="
                          isAllowedAdditionalService(turnaround.turnarounds, 'is_allowed_free_text')
                        "
                        :class="[$style['mission-turnarounds_col-input'], $style['col-input']]"
                      >
                        <input
                          v-model="service.booking_text"
                          placeholder="Description"
                          maxlength="255"
                          type="text"
                        />
                      </div>
                      <div
                        v-if="
                          isAllowedAdditionalService(
                            turnaround.turnarounds,
                            'is_allowed_quantity_selection'
                          )
                        "
                        :class="[$style['mission-turnarounds_col-input'], $style['col-input']]"
                      >
                        <input
                          v-model="service.booking_quantity"
                          placeholder="Quantity"
                          type="number"
                          min="0"
                        />
                        <span class="lowercase" :class="$style['col-input__prefix']">
                          {{ service?.service?.quantity_selection_uom?.code || 'KG' }}
                        </span>
                      </div>
                      <MissionTurnaroundsAction icon="comment-alt-regular" tooltip-text="Comment">
                        <template #dropdown-popper>
                          <InputField
                            v-model="service.note"
                            placeholder="Comment"
                            class="comment-input mb-0"
                          />
                        </template>
                      </MissionTurnaroundsAction>
                    </div>
                  </div>
                </td>
                <td>
                  <div
                    :class="[
                      $style['delete-service-btn'],
                      {
                        'opacity-50 !cursor-not-allowed': !checkPermissionForDeletion(turnaround)
                      }
                    ]"
                    @click="onDeleteService(turnaround)"
                  >
                    <img
                      :src="getImageUrl('assets/icons/delete.png')"
                      :class="$style['mission-itinerary__delete']"
                      alt="delete"
                    />
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
      <Button
        class="!my-4 !mx-3"
        :class="[
          $style['mission-turnarounds__service-btn'],
          $style['mission-turnarounds__service-btn--primary']
        ]"
        @click="onClickAddServiceRow"
      >
        <span>+ Add service row</span>
      </Button>
    </div>
    <div :class="$style['mission-turnarounds__actions']">
      <div class="flex items-center gap-x-2">
        <button
          data-bs-dismiss="modal"
          type="button"
          class="!bg-gray-200 !text-grey-900"
          :class="[$style['mission-turnarounds__service-btn']]"
        >
          Close
        </button>
        <button
          :class="[
            $style['mission-turnarounds__service-btn'],
            $style['mission-turnarounds__service-btn--submit']
          ]"
          @click="onUpdateGroundServicing"
        >
          Update Ground Servicing
        </button>
      </div>
    </div>
    <MissionTurnaroundLoading
      v-if="isUpdatingGroundServicing || isFetchingTurnarounds"
      class="absolute z-[100] left-0 top-0 w-full h-full"
    />
  </div>
</template>
<script setup lang="ts">
import { getImageUrl, getMissionId } from '@/helpers'
import { Button, InputField, CheckboxField } from 'shared/components'
import MissionTurnaroundsServiceSelect from '@/components/mission-turnarounds/MissionTurnaroundsServiceSelect.vue'
import MissionTurnaroundsAction from '@/components/mission-turnarounds/MissionTurnaroundsAction.vue'
import { useTurnaroundsStore } from '@/stores/useMissionTurnaroundsStore'
import { onMounted, ref, nextTick, computed } from 'vue'
import { storeToRefs } from 'pinia'
import type { IService } from '@/types/mission/mission-reference.types'
import { useFetch } from '@/composables/useFetch'
import MissionReferences from '@/services/mission/mission-references'
import MissionTurnarounds from '@/services/mission/mission-turnarounds'
import { mappedTurnarounds } from '@/helpers/turnarounds'
import MissionTurnaroundLoading from '@/components/mission-turnarounds/MissionTurnaroundLoading.vue'
import { findServiceById, isDisabledService } from '@/helpers/mission'
import { turnaroundNonEditableServices } from '@/constants/service.constants'
import type { ITurnaroundModel } from '@/types/mission-turnarounds/mission-turnarounds'

const TEMPRORARY_SERVICE_DATA = {
  // LOCATION: 800715,
  // ORGANISATION: 100653
}

const storeTurnarounds = useTurnaroundsStore()
const { missionForm, groundServicing, isFetchingTurnarounds, turnaroundsModel, generateServices } =
  storeToRefs(storeTurnarounds)

const groundServicingLength = computed(() =>
  groundServicing.value?.length ? groundServicing.value?.length + 1 : 0
)

const {
  loading: isLoadingServices,
  data: serviceOptions,
  callFetch: fetchServices
} = useFetch<IService[], (locationId: number, organisationId?: number) => void>(
  async (locationId: number, organisationId?: number) => {
    return await MissionReferences.fetchServices(locationId, organisationId)
  },
  []
)

const filterServiceOptions = (currentValue: number, existsValues: any[], options: any[]) => {
  return options.filter(
    (option) => !existsValues.find((value) => value.id === option.id) || option.id === currentValue
  )
}

const { loading: isUpdatingGroundServicing, callFetch: updateGroundServicing } = useFetch<
  IService[],
  (locationId: number, organisationId?: number) => void
>(async (missionId: number) => {
  const reducedTurnarounds = mappedTurnarounds(turnaroundsModel.value)
  return await MissionTurnarounds.updateGroundServicing(missionId, reducedTurnarounds)
})

const searchServiceQuery = ref('')
const onSearchService = (event: string) => {
  searchServiceQuery.value = event
}

const isAllowedAdditionalService = (turnarounds: any[], key) => {
  return turnarounds.some((service: any) => service?.service?.[key])
}

const onUpdateGroundServicing = async () => {
  await updateGroundServicing(getMissionId())
  await fetchData()

  // Close modal on successful submit
  const modal = document.getElementById('modal-xxl')
  if (modal) {
    modal.click()
  }
}

const checkPermissionForDeletion = (turnaround: ITurnaroundModel): boolean => {
  return !turnaroundNonEditableServices.some((serviceCode) =>
    turnaround.turnarounds?.map((t) => t?.service?.codename).find((t) => t === serviceCode)
  )
}

const onDeleteService = async (turnaround: ITurnaroundModel) => {
  if (!checkPermissionForDeletion(turnaround)) return
  let isConfirmed = !isExistsService(turnaround.id)

  if (!isConfirmed) {
    const result = await window.Swal({
      title: 'Delete service',
      text: 'Please confirm you want to remove service',
      icon: 'info',
      showCancelButton: true
    })
    isConfirmed = result.isConfirmed
  }

  isConfirmed && (turnaround.is_deleted = true)
}

const isExistsService = (turnaroundId: number) => {
  if (turnaroundsModel.value.length === generateServices.value.length) {
    return true
  }
  return !!generateServices.value.find((service) => service.id === turnaroundId)
}

const isServiceSelectDisabled = (turnaroundId: number) => {
  return isExistsService(turnaroundId)
}

const tableWrapperRef = ref<HTMLElement | null>(null)
const scrollToTableWrapperBottom = () => {
  if (!tableWrapperRef.value) {
    return
  }
  const { scrollHeight } = tableWrapperRef.value
  tableWrapperRef.value.scroll(0, scrollHeight)
}

const onClickAddServiceRow = () => {
  turnaroundsModel.value.push({
    id: null,
    is_deleted: false,
    turnarounds: Array.from({ length: groundServicingLength.value - 1 }).map((_, index) => {
      return {
        id: groundServicing.value[index]?.id,
        on_arrival: false,
        on_departure: false,
        booking_text: '',
        booking_quantity: 0,
        note: '',
        service: []
      }
    })
  })

  nextTick(scrollToTableWrapperBottom)
}

const fetchData = async () => {
  const missionId = getMissionId()

  if (!missionId) {
    return
  }

  await Promise.allSettled([
    storeTurnarounds.fetchTurnarounds(missionId),
    storeTurnarounds.fetchMissionTurnarounds(missionId)
  ])
  await fetchServices(TEMPRORARY_SERVICE_DATA.LOCATION, missionForm.value?.organisation.id)
}

onMounted(fetchData)
</script>
<style scoped lang="scss">
.comment-input {
  :deep(.u-input-wrapper) {
    @apply border-none focus:shadow-none rounded-none #{!important};
  }
}
</style>

<style module lang="scss">
.mission-turnarounds {
  @apply relative flex flex-col bg-white min-w-0 rounded-[0.5rem] pb-2;

  &__title {
    @apply text-center text-xs text-grey-900 py-2 #{!important};
  }

  .service-table {
    @apply w-full;

    //general style for table
    th,
    td {
      @apply p-1.5 text-xs border-r border-grey-opacity-800/25;
      &:not(:last-child) {
        @apply min-w-[8rem];
      }
    }

    tr {
      @apply border-t-0 #{!important};
    }

    // style for table header
    thead {
      .service-table__header-row {
        @apply bg-grey-50 border-t border-gray-50;
        th {
          @apply border-r-0 px-0 text-center text-grey-900;
        }

        &:first-child {
          @apply border-t-0 overflow-hidden;
        }

        &:nth-child(2) {
          th {
            @apply text-start;
          }
        }

        th:first-child {
          @apply min-w-[200px] text-start;
        }
      }
    }

    // style for table body
    tbody {
      .service-table__body-row {
        td {
          @apply text-center border border-grey-opacity-800/25;
        }

        .delete-service-btn {
          @apply w-6 h-6 mx-auto shadow-none cursor-pointer;
          img {
            filter: invert(33%) sepia(41%) saturate(6873%) hue-rotate(330deg) brightness(85%)
              contrast(110%);
          }
        }
      }
    }
  }

  .col-input {
    @apply max-w-[20rem] mx-auto pl-2 leading-6 w-full h-fit overflow-hidden flex items-center appearance-none text-[0.875rem] bg-clip-padding  bg-white font-normal focus:outline-none text-grey-700 border-grey-100 border-[0.0625rem] border-solid rounded-[0.5rem] #{!important};

    input {
      @apply border-0 shadow-none outline-none w-full #{!important};
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.07);
      transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    }

    &__prefix {
      @apply bg-grey-50 px-2;
    }
  }

  &__actions {
    @apply flex items-center justify-end mt-2;
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

.confirm-delete-actions {
  button {
    @apply bg-red-500 #{!important};
  }
}
</style>