<template>
  <div class="w-full h-auto flex flex-col gap-2">
    <div class="servicing-step bg-white w-full border border-transparent rounded-md">
      <div class="servicing-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="servicing-step-header-name">Supplier Order</div>
      </div>
      <div class="servicing-step-content compliance-status w-full flex flex-col p-[0.75rem] gap-2">
        <div class="w-full flex gap-2">
          <div class="servicing-step-content-el-name flex items-center w-[140px]">
            AML Buying Company
          </div>
          <div class="servicing-step-content-el-value py-[0.25rem] px-[0.75rem]">
            AML Global Limited
          </div>
        </div>
        <div class="w-full flex gap-2">
          <div class="servicing-step-content-el-name flex items-center w-[140px]">Status</div>
          <div class="servicing-step-content-el-status py-[0.25rem] px-[0.75rem] ml-[0.75rem]">
            Approval required
          </div>
        </div>
      </div>
    </div>
    <div class="servicing-step bg-white w-full border border-transparent rounded-md">
      <div class="servicing-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="servicing-step-header-name">Ground Handling Services</div>
        <div>
          <div v-if="isConfirming" class="loading-wrap">
            <Loading />
          </div>
          <div v-else class="flex items-center gap-[0.5rem]">
            <div class="clock-wrapper">
              <img src="../../assets/icons/clock.svg" alt="add" />
            </div>
            <div>
              <span class="service-count">{{ confirmedServiceCount }}</span>
              <span class="service-count service-count-secondary">{{ confirmedServiceText }}</span>
            </div>
          </div>
        </div>
      </div>
      <div v-if="true" class="servicing-step-content">
        <div class="servicing-step-content-header-sub flex h-[30px]">
          <div
            class="servicing-step-content-header-sub-wrap flex w-6/12 py-[0.5rem] pl-[0.75rem] gap-2"
          >
            <div class="servicing-step-content-header-sub-el flex w-6/12 justify-start">Item</div>
            <div
              class="servicing-step-content-header-sub-el flex w-6/12 justify-start el-border pl-4"
            >
              Quantity
            </div>
          </div>
          <div class="servicing-step-content-header-sub-wrap flex w-6/12 py-[0.5rem]">
            <div
              class="servicing-step-content-header-sub-el flex w-full justify-center items-center"
            >
              Arrival
            </div>
            <div
              class="servicing-step-content-header-sub-el flex w-full justify-center el-border items-center"
            >
              Departure
            </div>
            <div
              class="servicing-step-content-header-sub-el flex w-full justify-center items-center"
            >
              Confirmed?
            </div>
          </div>
        </div>
        <div
          v-if="isLoadingSupplierOrderServices"
          class="flex justify-center items-center w-full h-[60px]"
        >
          <Loading />
        </div>
        <div
          v-for="service in supplierOrderServices ?? []"
          :key="service.id"
          class="servicing-step-content-element flex"
          :style="{ 'background-color': service.is_confirmed ? 'rgba(34, 225, 110, 0.08)' : '' }"
        >
          <div
            class="servicing-step-content-element-wrap flex w-6/12 py-[0.5rem] pl-[0.75rem] el-border-light"
          >
            <div
              class="servicing-step-content-element-el-name flex justify-start items-center w-6/12"
            >
              {{ service.handling_service?.full_repr }}
            </div>
            <div class="servicing-step-content-element-el flex justify-start items-center w-6/12">
              <span class="text-light-subtitle pr-[20px] text-[0.75rem]">x</span>
              {{ getServiceQuantityText(service) }}
            </div>
          </div>
          <div class="servicing-step-content-element-wrap flex w-6/12 el-border-light">
            <div
              class="servicing-step-content-element-el-name flex justify-center items-center w-full"
            >
              <CheckboxField
                v-model="service.applies_on_arrival"
                disabled
                class="mb-0"
                :size="'20px'"
                :background-color="service.is_confirmed ? 'rgba(34, 225, 110, 0.08)' : ''"
              ></CheckboxField>
            </div>
            <div
              class="servicing-step-content-element-el el-border-light flex justify-center items-center w-full"
            >
              <CheckboxField
                v-model="service.applies_on_departure"
                disabled
                class="mb-0"
                :size="'20px'"
                :background-color="service.is_confirmed ? 'rgba(34, 225, 110, 0.08)' : ''"
              ></CheckboxField>
            </div>
            <div
              class="servicing-step-content-element-el-name flex justify-center items-center w-full"
            >
              <CheckboxField
                v-model="service.is_confirmed"
                :disabled="
                  service.handling_service.id === 353 || isConfirming || service.is_confirmed
                "
                class="mb-0"
                :size="'20px'"
                :background-color="service.is_confirmed ? 'rgba(34, 225, 110, 0.08)' : ''"
                @update:model-value="onConfirmService(service.id)"
              ></CheckboxField>
            </div>
          </div>
        </div>
        <AddServiceToOrder v-if="orderId" :order="order" :current-tab="2" />
      </div>
    </div>
    <ClientDocuments />
    <div
      v-if="!order?.fuel_order?.is_open_release"
      class="servicing-step bg-white w-full border border-transparent rounded-md"
    >
      <div class="servicing-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="servicing-step-header-name">Flight Tracking</div>
      </div>
      <div class="servicing-step-content w-full flex gap-2">
        <div class="order-leaflet-map h-[375px] w-full rounded-bl-md rounded-br-md">
          <FlightTracking
            :airport-from="airportFrom"
            :airport-to="airportTo"
            :aircraft-locations="aircraftLocations"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, type PropType, ref } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { useMutationConfirmSupplierOrderService } from '@/services/mutations';
import { useQuerySupplierOrderServices } from '@/services/queries';
import { getServiceQuantityText } from '@/helpers/services';
import AddServiceToOrder from '../datacomponent/AddServiceToOrder.vue';
import ClientDocuments from '../datacomponent/ClientDocuments.vue';
import FlightTracking from '../datacomponent/FlightTracking.vue';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import Loading from '../forms/Loading.vue';

import type { IOrder } from 'shared/types';

const props = defineProps({
  isActive: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  order: {
    type: Object as PropType<IOrder>,
    default: null
  }
});

const queryClient = useQueryClient();

const airportFrom: any = ref(null);
const airportTo: any = ref(null);
const aircraftLocations: any = ref(null);

const orderId = computed(() => props.order?.id);
const isTabActive = computed(() => !!props.isActive);

const { data: supplierOrderServices, isLoading: isLoadingSupplierOrderServices } =
  useQuerySupplierOrderServices(orderId, {
    enabled: isTabActive
  });

const { mutate: confirmSupplierOrderServiceMutation, isPending: isConfirming } =
  useMutationConfirmSupplierOrderService();

const confirmedServiceCount = computed(
  () => supplierOrderServices?.value?.filter((service) => service.is_confirmed).length ?? 0
);
const totalServiceCount = computed(() => supplierOrderServices?.value?.length ?? 0);
const confirmedServiceText = computed(() => {
  const serviceText = totalServiceCount.value === 1 ? 'service' : 'services';
  return `/${totalServiceCount.value} ${serviceText} confirmed`;
});

const onConfirmService = async (serviceId: number) => {
  await confirmSupplierOrderServiceMutation(
    {
      orderId: Number(orderId.value),
      serviceId
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['supplierOrderServices', orderId.value] });
      }
    }
  );
};
</script>

<style lang="scss">
.servicing-step {
  .button {
    background-color: rgba(81, 93, 138, 1) !important;
    color: white !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-[0.5rem] px-[1rem] rounded-lg #{!important};

    &:disabled {
      background-color: rgb(190, 196, 217) !important;
      color: rgb(133, 141, 173) !important;
      border: transparent !important;
    }

    &.light-button {
      background-color: rgba(240, 242, 252, 1) !important;
      border: transparent !important;
      padding: 0.5rem !important;
    }

    &-cancel-service {
      background-color: rgba(255, 255, 255, 1) !important;
      padding-left: 0.5rem !important;
      padding-right: 0.5rem !important;
      img {
        filter: brightness(0) saturate(100%) invert(35%) sepia(15%) saturate(1184%)
          hue-rotate(190deg) brightness(98%) contrast(92%);
      }
    }
  }

  .download-button {
    background-color: rgba(240, 242, 252, 1);
    border-color: transparent;
    border-radius: 12px;
    box-shadow: none;
    padding: 10px;
  }

  .el-border {
    border-right: 1px solid rgb(223, 226, 236);

    &-light {
      border-right: 1px solid theme('colors.dark-background');
    }
  }

  .hover-wrap {
    &:hover {
      .servicing-step-tooltip {
        display: block;
      }
    }
  }

  &-add-service {
    color: rgba(81, 93, 138, 1);
    font-weight: 500;
    font-size: 14px;
    img {
      filter: brightness(0) saturate(100%) invert(36%) sepia(11%) saturate(1776%) hue-rotate(190deg)
        brightness(94%) contrast(86%);
    }
  }

  &-tooltip {
    display: none;
    position: absolute;
    background-color: rgb(81, 93, 138);
    color: rgb(255, 255, 255);
    font-size: 12px;
    font-weight: 400;
    z-index: 10;
    padding: 0.5rem;
    border-radius: 0.5rem;
    top: 2.5rem;
    right: 0;
    min-width: 30vw;

    &::before {
      content: '';
      position: absolute;
      width: 10px;
      height: 10px;
      background-color: rgb(81, 93, 138);
      transform: rotate(45deg);
      right: 1.9rem;
      top: -5px;
    }

    &.right-tooltip {
      left: 0;
      top: 1.6rem;
      min-width: 10vw;

      &::before {
        right: 0;
        left: 1rem;
      }
    }
  }

  &-header {
    color: theme('colors.main');
    font-size: 18px;
    font-weight: 600;
  }

  &-content {
    &-data-wrap {
      border-bottom: 1px solid theme('colors.dark-background');
      background-color: rgba(246, 248, 252, 0.5);

      &:last-of-type {
        border-radius: 0 0 8px 8px;
      }

      &.selected-supplier {
        background-color: rgba(255, 255, 255, 1) !important;

        .servicing-step-content-col-data {
          color: rgba(39, 44, 63, 1);
          background-color: rgba(255, 255, 255, 1);

          .warn {
            filter: none;
          }

          .selection-tick {
            display: flex;
            border-radius: 12px;
            background-color: rgba(11, 161, 125, 0.15);
            height: 40px;
            width: 40px;
            opacity: 1;
          }
        }
      }
    }

    &-header-wrap {
      background-color: rgb(246, 248, 252);
    }

    &-header-big-wrap {
      background-color: rgba(246, 248, 252, 1);
    }

    &-header-big {
      &-el {
        background-color: rgba(223, 226, 236, 0.5);
        color: rgba(39, 44, 63, 1);
        font-size: 12px;
        font-weight: 500;
      }
    }

    &-header-sub {
      background-color: rgba(246, 248, 252, 1);

      &-el {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
      }
    }

    &-el {
      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 13px;
        font-weight: 500;
        min-width: 100px;
      }

      &-value {
        color: theme('colors.main');
        font-size: 14px;
        font-weight: 500;
      }

      &-status {
        background-color: rgba(11, 161, 125, 1);
        color: rgb(255, 255, 255);
        border-radius: 6px;
        border: 1px solid transparent;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;

        &-warn {
          background-color: rgba(254, 161, 22, 1);
          color: rgb(255, 255, 255);
          border-radius: 6px;
          border: 1px solid transparent;
          font-size: 12px;
          font-weight: 500;
          text-transform: uppercase;
        }
      }
    }

    &-element {
      height: 60px;

      &-wrap {
        border-bottom: 1px solid rgba(239, 241, 246, 1);
      }

      &-el {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 400;

        &-name {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 500;
        }
      }
    }

    &-results {
      background-color: rgba(246, 248, 252, 1);

      &-el {
        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 11px;
          font-weight: 500;
          border-left: 1px solid rgb(223, 226, 236);
        }

        &-value {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 600;
        }
      }
    }

    &-divider {
      text-transform: capitalize;
      background-color: rgba(246, 248, 252, 1);
      color: rgba(82, 90, 122, 1);
      font-size: 12px;
      font-weight: 500;
    }

    &-margin {
      &-name {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 500;
      }

      &-value {
        color: rgba(11, 161, 125, 1);
        font-size: 16px;
        font-weight: 600;
      }
    }

    &-col {
      height: 100%;

      &-header {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
        background-color: rgb(246, 248, 252);
      }

      &-data {
        color: rgba(133, 141, 173, 1);
        font-size: 13px;
        font-weight: 400;

        .warn {
          filter: brightness(0) saturate(100%) invert(89%) sepia(7%) saturate(740%)
            hue-rotate(193deg) brightness(88%) contrast(92%);
        }

        .selection-tick {
          opacity: 0;
          height: 40px;
          width: 40px;
        }

        .files-button {
          border: 1px solid rgba(223, 226, 236, 1);
          border-radius: 6px;
        }

        .horizontal {
          transform: rotate(90deg);
        }

        &.status-badge {
          color: rgba(255, 255, 255) !important;

          &-recieved {
            background-color: rgba(11, 161, 125, 0.12) !important;
            color: rgba(11, 161, 125, 1) !important;
          }
          &-requested {
            background-color: rgba(254, 161, 22, 0.12) !important;
            color: rgba(254, 161, 22, 1) !important;
          }
        }
      }
    }

    &-none {
      position: relative;
      background-color: rgba(255, 161, 0, 0.08);

      &-header {
        color: theme('colors.main');
        font-size: 14px;
        font-weight: 600;
      }

      &-desc {
        color: theme('colors.main');
        font-size: 12px;
        font-weight: 400;
      }

      .warn {
        position: absolute;
        left: 0.75rem;
      }
    }

    &-missing {
      background-color: rgba(246, 248, 252, 1);

      span {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
      }
    }
  }
}

.clock-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: theme('colors.yellow.600');
  border-radius: 50%;
  width: 20px;
  height: 20px;
}

.service-count {
  color: theme('colors.base.800');
  font-weight: 500;
  font-size: 13px;
  line-height: 18px;
}

.service-count-secondary {
  color: theme('colors.base.600');
  font-weight: 400;
}
</style>
