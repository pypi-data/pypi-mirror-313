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
        <div class="loading-wrap">
          <Loading v-if="false" />
        </div>
      </div>
      <div v-if="true" class="servicing-step-content">
        <div class="servicing-step-content-header-sub flex">
          <div
            class="servicing-step-content-header-sub-wrap flex w-8/12 py-[0.5rem] pl-[0.75rem] gap-2"
          >
            <div class="servicing-step-content-header-sub-el flex w-6/12 justify-start">Item</div>
            <div
              class="servicing-step-content-header-sub-el flex w-6/12 justify-start el-border pl-4"
            >
              Quantity
            </div>
          </div>
          <div class="servicing-step-content-header-sub-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]">
            <div class="servicing-step-content-header-sub-el flex w-full justify-center">
              Arrival
            </div>
            <div class="servicing-step-content-header-sub-el flex w-full justify-center">
              Departure
            </div>
            <div class="servicing-step-content-header-sub-el flex w-full justify-start">&nbsp;</div>
          </div>
        </div>
        <div
          v-for="(service, index) in mockServices"
          :key="index"
          class="servicing-step-content-element flex"
          :style="{ 'background-color': service.green ? 'rgba(34, 225, 110, 0.08)' : '' }"
        >
          <div
            class="servicing-step-content-element-wrap flex w-8/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="servicing-step-content-element-el-name flex justify-start items-center w-6/12"
            >
              {{ service.name }}
            </div>
            <div class="servicing-step-content-element-el flex justify-start items-center w-6/12">
              <span class="text-light-subtitle pr-[0.5rem] text-[0.75rem]">x</span>
              {{ service.quantity ?? '--' }}
              {{ service.time ?? '' }}
            </div>
          </div>
          <div
            class="servicing-step-content-element-wrap flex w-4/12 py-[0.75rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="servicing-step-content-element-el-name flex justify-center items-center w-full"
            >
              <CheckboxField
                v-model="service.arrival"
                class="mb-0 mr-1"
                :size="'20px'"
                :background-color="service.green ? 'rgba(34, 225, 110, 0.08)' : ''"
              ></CheckboxField>
            </div>
            <div class="servicing-step-content-element-el flex justify-center items-center w-full">
              <CheckboxField
                v-model="service.departure"
                class="mb-0 mr-1"
                :size="'20px'"
                :background-color="service.green ? 'rgba(34, 225, 110, 0.08)' : ''"
              ></CheckboxField>
            </div>
            <div
              class="servicing-step-content-element-el flex justify-center items-center w-full px-[0.5rem]"
            >
              <img
                width="20"
                height="20"
                src="../../assets/icons/edit.svg"
                alt="comment"
                class="cursor-pointer"
              />
            </div>
          </div>
        </div>
        <div
          v-for="(newService, index) in newServices"
          :key="index"
          class="servicing-step-content-element flex"
        >
          <div
            class="servicing-step-content-element-wrap flex w-8/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="servicing-step-content-element-el-name flex justify-center items-center w-6/12"
            >
              <SelectField
                class="w-full mb-0"
                :is-white="true"
                placeholder="Choose Service"
                :options="displayServices"
                label="name"
                :model-value="newService.name"
                @update:model-value="
                  (value) => {
                    newService.name = value;
                  }
                "
                @search="handleServiceSearch($event)"
              />
            </div>
            <div class="servicing-step-content-element-el flex justify-start items-center w-6/12">
              <div class="input-wrap flex items-center pr-[0.75rem]">
                <span class="text-light-subtitle pr-[0.5rem] text-[0.75rem]">x</span>
                <InputField
                  :model-value="newService.quantity"
                  class="w-6/12 mb-0"
                  :is-white="true"
                  :is-half="true"
                  placeholder=" "
                  @update:model-value="
                    (value) => {
                      newService.quantity = value;
                    }
                  "
                />
                <SelectField
                  class="w-6/12 mb-0"
                  :is-white="true"
                  :is-half="true"
                  placeholder=" "
                  :options="['Minutes', 'Hours', 'Days']"
                  label="description_short"
                  :model-value="newService.time"
                  @update:model-value="
                    (value) => {
                      newService.time = value;
                    }
                  "
                />
              </div>
            </div>
          </div>
          <div
            class="servicing-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="servicing-step-content-element-el-name flex justify-center items-center w-full"
            >
              <CheckboxField
                v-model="newService.arrival"
                class="mb-0 mr-1"
                :size="'20px'"
              ></CheckboxField>
            </div>
            <div class="servicing-step-content-element-el flex justify-center items-center w-full">
              <CheckboxField
                v-model="newService.departure"
                class="mb-0 mr-1"
                :size="'20px'"
              ></CheckboxField>
            </div>
            <div
              class="servicing-step-content-element-el flex justify-between items-center w-full px-[0.5rem]"
            >
              <img
                width="20"
                height="20"
                src="../../assets/icons/edit.svg"
                alt="comment"
                class="cursor-pointer"
              />
              <img
                width="20"
                height="20"
                src="../../assets/icons/cross-red.svg"
                alt="delete"
                class="cursor-pointer"
                @click="deleteService(index)"
              />
            </div>
          </div>
        </div>
        <div
          class="servicing-step-add-service flex cursor-pointer p-[0.75rem] gap-2 w-fit"
          @click="addNewService"
        >
          <img src="../../assets/icons/plus.svg" alt="add" />
          Add Service to Order
        </div>
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
import { computed, type PropType, type Ref, ref, watch } from 'vue';
import ClientDocuments from '../datacomponent/ClientDocuments.vue';
import FlightTracking from '../datacomponent/FlightTracking.vue';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import Loading from '../forms/Loading.vue';

import type { IOrder } from 'shared/types';

const props = defineProps({
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  order: {
    type: Object as PropType<IOrder>,
    default: null
  }
});

const mockServices = ref([
  { name: 'Handling Fee', quantity: null, time: null, arrival: true, departure: true, green: true },
  { name: 'Passenger Handling', quantity: null, time: null, arrival: true, departure: false },
  { name: 'Parking', quantity: 3, time: 'Hours', arrival: true, departure: true }
]);

const airportFrom: any = ref(null);
const airportTo: any = ref(null);
const aircraftLocations: any = ref(null);

const userService = ref([{ name: '' }]);
const displayServices = computed(() => [...userService.value]);

const newServices: Ref<Array<any>> = ref([]);

const addNewService = () => {
  newServices.value.push({
    name: '',
    quantity: null,
    time: null,
    arrival: false,
    departure: false
  });
};

const deleteService = (id: number) => {
  newServices.value.splice(id, 1);
};

// const { callFetch: fetchHandlingServices, data: handlingServices } = useFetchHandlingServices();

const handleServiceSearch = (searchTerm: string) => {
  // console.log(searchTerm, index);
  userService.value = [{ name: searchTerm }];
};

watch(
  () => props.order,
  async (order: IOrder) => {
    if (order && order.id && order.type.is_gh) {
      // await fetchHandlingServices(order?.id);
    }
  }
);
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
      &-wrap {
        border-bottom: 1px solid rgba(246, 248, 252, 1);
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
</style>
