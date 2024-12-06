<template>
  <div class="w-full h-auto flex flex-col gap-2">
    <div class="w-full h-full flex gap-2">
      <div class="order-step bg-white w-6/12 border border-transparent rounded-md">
        <div class="order-step-header flex justify-between py-[1rem] px-[0.75rem]">
          <div class="order-step-header-name">Supplier Order</div>
        </div>
        <div class="order-step-content compliance-status w-full flex flex-col p-[0.75rem] gap-2">
          <div class="w-full flex gap-2">
            <div class="order-step-content-el-name flex items-center w-[140px]">
              AML Buying Company
            </div>
            <div class="order-step-content-el-value py-[0.25rem] px-[0.75rem]">
              AML Global Limited
            </div>
          </div>
          <div class="w-full flex gap-2">
            <div class="order-step-content-el-name flex items-center w-[140px]">Status</div>
            <div class="order-step-content-el-status py-[0.25rem] px-[0.75rem] ml-[0.75rem]">
              Approval required
            </div>
          </div>
        </div>
      </div>
      <div class="order-step bg-white w-6/12 border border-transparent rounded-md">
        <div class="order-step-header flex justify-between py-[1rem] px-[0.75rem]">
          <div class="order-step-header-name">Client Order</div>
        </div>
        <div class="order-step-content compliance-status w-full flex flex-col p-[0.75rem] gap-2">
          <div class="w-full flex gap-2">
            <div class="order-step-content-el-name flex items-center w-[140px]">
              AML Selling Company
            </div>
            <div class="order-step-content-el-value py-[0.25rem] px-[0.75rem]">AML Global OU</div>
          </div>
          <div class="w-full flex gap-2">
            <div class="order-step-content-el-name flex items-center w-[140px]">Fuel Release</div>
            <div class="order-step-content-el-status-warn py-[0.25rem] px-[0.75rem] ml-[0.75rem]">
              Waiting on supplier confirmation
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="order?.fuel_order?.is_open_release"
      class="order-step bg-white w-full border border-transparent rounded-md"
    >
      <div class="order-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="order-step-header-name">Client Credit Exposure</div>
      </div>
      <div class="order-step-content w-full flex p-[0.75rem] gap-2">
        <CreditExposure />
      </div>
    </div>
    <div class="order-step bg-white w-full border border-transparent rounded-md">
      <div class="order-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="order-step-header-name">Uplifts</div>
      </div>
      <div v-if="isPendingFuelUplifts" class="order-step-content w-full flex flex-col py-[1.25rem]">
        <Loading />
      </div>
      <div v-else-if="fuelUplifts" class="order-step-content w-full flex flex-col">
        <div class="order-step-content-header-wrap w-full flex items-center">
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Date & Time</div>
          </div>
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Aircraft</div>
          </div>
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">
              Quantity Uplifted
            </div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Destination</div>
          </div>
          <div class="order-step-content-col w-1/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">
              Delivery Ticket
            </div>
          </div>
        </div>
        <div
          v-for="uplift in fuelUplifts"
          :key="uplift.id"
          class="order-step-content-data-wrap selected-supplier w-full flex items-center"
        >
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ toLocalTime(uplift.time_z) }}
            </div>
          </div>
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ uplift.tail_number?.full_repr ?? '' }}
            </div>
          </div>
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{
                `${uplift.fuel_quantity} ${uplift.fuel_uom?.description_plural} ${uplift.fuel_type?.name}`
              }}
            </div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ uplift.destination_int_dom }}
            </div>
          </div>
          <div class="order-step-content-col w-1/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
              <a
                v-if="uplift.file"
                :title="getFilenameByUrl(uplift.file)"
                :href="uplift.file"
                download
              >
                <Button class="download-button">
                  <img
                    width="20"
                    height="20"
                    src="../../assets/icons/download.svg"
                    alt="options"
                    class="horizontal cursor-pointer" /></Button
              ></a>
              <span v-else class="pl-[14px]">--</span>
            </div>
          </div>
        </div>
      </div>
      <div
        v-else-if="isEmptyFuelUplifts"
        class="order-step-content-missing w-full flex justify-center align-center py-[1.25rem]"
      >
        <span>No uplift details received</span>
      </div>
    </div>
    <FuelPricingDetails
      v-for="(uplift, upliftId) in fuelUplifts"
      :key="uplift.id"
      :order="props.order"
      :is-loading="isLoadingOrderPricing"
      :is-loading-update-order-pricing="isLoadingUpdateOrderPricing"
      :uplift-index="upliftId"
      :uplift-id="uplift.id"
      :uplift-date="uplift.time_z"
      :uplift-pricing-obj="fuelUpliftPricings"
      multiple-uplifts
      :uplift-pricing="fuelUpliftPricings?.uplifts_pricing![uplift.id]"
    />
    <div
      v-if="fuelUpliftPricings && fuelUplifts && fuelUplifts.length > 0"
      class="order-step bg-white w-full border border-transparent rounded-md"
    >
      <div class="order-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="order-step-header-name">Total Margin - Actual Uplift(s)</div>
      </div>
      <div
        v-if="isPendingFuelUpliftPricings"
        class="order-step-content w-full flex flex-col py-[1.25rem]"
      >
        <Loading />
      </div>
      <div class="order-step-content w-full flex flex-col">
        <div class="order-step-content-results flex">
          <div class="order-step-content-results-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]"></div>
          <div class="order-step-content-results-wrap flex w-4/12 py-[0.5rem]">
            <div
              class="order-step-content-results-el-name flex items-center w-full p-1 pl-[0.75rem] justify-start items-center"
            >
              Total Buy Price
            </div>
            <div
              class="order-step-content-results-el-value flex w-full p-1 justify-start items-center"
            >
              {{ formatNumber(fuelUpliftPricings?.pricing_summary?.supplier_total.toString()) }}
              {{
                fuelUpliftPricings?.uplifts_pricing[fuelUplifts![0].id].fuel_pricing?.supplier
                  ?.amount_currency?.code
              }}
            </div>
          </div>
          <div class="order-step-content-results-wrap flex w-4/12 py-[0.5rem]">
            <div
              class="order-step-content-results-el-name flex items-center w-full p-1 pl-[0.75rem] justify-start items-center"
            >
              Total Sell Price
            </div>
            <div
              class="order-step-content-results-el-value flex w-full p-1 justify-start items-center"
            >
              {{ formatNumber(fuelUpliftPricings?.pricing_summary?.client_total.toString()) }}
              {{
                fuelUpliftPricings?.uplifts_pricing[fuelUplifts![0].id].fuel_pricing?.client
                  ?.amount_currency?.code
              }}
            </div>
          </div>
        </div>
        <div class="order-step-content-margin flex p-3">
          <div class="order-step-content-margin-name w-6/12 flex items-center">
            Total Order Margin
          </div>
          <div class="order-step-content-margin-value w-6/12 flex items-center pl-2">
            {{ formatNumber(fuelUpliftPricings?.pricing_summary?.margin_amount) }}
            {{
              fuelUpliftPricings?.uplifts_pricing[fuelUplifts![0].id].fuel_pricing?.client
                ?.amount_currency?.code
            }}
            ({{ fuelUpliftPricings?.pricing_summary?.margin_percentage }}%)
          </div>
        </div>
      </div>
    </div>
    <RoiCalculation
      v-if="fuelUpliftPricings && fuelUplifts && fuelUplifts.length > 0"
      :order="props.order"
      :order-roi="orderRoi"
      :order-roi-days="fuelUpliftPricings!.terms_days ?? DEFAULT_ORDER_ROI_DAYS"
      :order-pricing="orderPricing"
      :is-loading="isLoadingOrderPricing"
      :is-loading-update-order-roi="isLoadingUpdateOrderRoi && isPendingFuelUpliftPricings"
      :uplift-pricing-obj="fuelUpliftPricings"
      @update:roi="onRoiChange"
    />
    <ClientDocuments />
    <div
      v-if="!order?.fuel_order?.is_open_release"
      class="order-step bg-white w-full border border-transparent rounded-md"
    >
      <div class="order-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="order-step-header-name">Flight Tracking</div>
      </div>
      <div class="order-step-content w-full flex gap-2">
        <div
          v-if="currentStep === 3"
          class="order-leaflet-map h-[375px] w-full rounded-bl-md rounded-br-md"
        >
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
import { computed, onMounted, type PropType, ref, toRefs, watch } from 'vue';
import { Button } from 'shared/components';
import { useFetch } from 'shared/composables';
import { useOrderReferenceStore } from '@/stores/useOrderReferenceStore';
import { useOrderStore } from '@/stores/useOrderStore';
import OrderReferences from '@/services/order/order-references';
import { useQueryFuelUplifts, useQueryUpliftFuelPricings } from '@/services/queries/uplift';
import { getFilenameByUrl } from '@/helpers/files';
import { formatNumber, toLocalTime } from '@/helpers/order';
import { DEFAULT_ORDER_ROI_DAYS } from '@/constants/order.constants';
import {
  CreditExposure,
  FlightTracking,
  FuelPricingDetails,
  RoiCalculation
} from '../datacomponent';
import ClientDocuments from '../datacomponent/ClientDocuments.vue';
import Loading from '../forms/Loading.vue';

import type { IFuelUplift, IOrder } from 'shared/types';

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

const orderStore = useOrderStore();
const orderReferenceStore = useOrderReferenceStore();

const {
  isLoadingOrderPricing,
  isLoadingUpdateOrderPricing,
  isLoadingUpdateOrderRoi,
  onRoiChange,
  orderPricing,
  orderRoi
} = toRefs(orderReferenceStore);

const currentStep = computed(() => orderStore.currentStep);
const isCurrentStep = computed(() => currentStep.value === 3 && orderStore.order?.type?.is_fuel);
const isUpliftsAvailable = ref(false);

const airportFrom: any = ref(null);
const airportTo: any = ref(null);
const aircraftLocations: any = ref(null);

const orderId = computed(() => orderStore.order?.id);

const { callFetch: fetchFlightAirportLocation } = useFetch<any>(async (id: number) => {
  const data = await OrderReferences.fetchFlightAirportLocations(id);
  if (typeof data === 'object') {
    airportFrom.value = data.arrival_from;
    airportTo.value = data.location;
  }
});

const { callFetch: fetchFlightAircraftLocation } = useFetch<any>(async (id: number) => {
  const data = await OrderReferences.fetchFlightAircraftLocations(id);
  if (typeof data === 'object') {
    const mappedData = data.aircraft_positions.map((el: any) => {
      return [el.latitude, el.longitude];
    });
    aircraftLocations.value = { ...data, latLng: mappedData };
  }
});

const {
  data: fuelUplifts,
  isPending: isPendingFuelUplifts,
  isError: isErrorFuelUplifts
} = useQueryFuelUplifts(orderId, {
  enabled: isCurrentStep,
  retry: false
});

const { data: fuelUpliftPricings, isPending: isPendingFuelUpliftPricings } =
  useQueryUpliftFuelPricings(orderId, {
    enabled: isUpliftsAvailable,
    retry: false
  });

const isEmptyFuelUplifts = computed(
  () => isErrorFuelUplifts || (!isPendingFuelUplifts.value && !fuelUplifts?.value?.length)
);

watch(
  () => fuelUpliftPricings.value,
  (value) => {
    if (value) {
      onRoiChange.value(value.terms_days.client_terms_days.toString(), true, value);
    }
  }
);

watch(
  () => [fuelUplifts.value, isCurrentStep.value],
  ([uplifts, step]) => {
    if (step && uplifts && (uplifts as IFuelUplift[]).length > 0) {
      isUpliftsAvailable.value = true;
    }
  }
);

watch(
  () => isUpliftsAvailable.value,
  (value) => {
    console.log(value);
  }
);

onMounted(async () => {
  // Replace when the backend is done
  await fetchFlightAirportLocation(1194);
  await fetchFlightAircraftLocation(1194);
});
</script>

<style lang="scss">
.order-step {
  .button {
    background-color: rgba(81, 93, 138, 1) !important;
    color: white !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-2 px-[1rem] rounded-xl #{!important};
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

  .el-border-left {
    border-left: 1px solid rgb(223, 226, 236);

    &-light {
      border-right: 1px solid theme('colors.dark-background');
    }
  }

  &-header {
    color: theme('colors.main');
    font-size: 18px;
    font-weight: 600;
  }

  &-content {
    &.compliance-status {
      border-top: 1px solid theme('colors.dark-background');
    }

    &-missing {
      background-color: rgba(246, 248, 252, 1);

      span {
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

    &-data-wrap {
      border-bottom: 1px solid theme('colors.dark-background');
      background-color: rgba(255, 255, 255, 1);
    }

    &-header-wrap {
      background-color: rgb(246, 248, 252);
    }

    &-header-big-wrap {
      background-color: rgba(246, 248, 252, 1);
    }

    &-divider {
      text-transform: capitalize;
      background-color: rgba(246, 248, 252, 1);
      color: rgba(82, 90, 122, 1);
      font-size: 12px;
      font-weight: 500;
    }

    &-results {
      border: 1px solid rgb(239, 241, 246);

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
      &-header {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
        background-color: rgb(246, 248, 252);
      }

      &-data {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 400;
        background-color: rgba(256, 256, 256, 1);

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 13px;
          font-weight: 500;
        }

        &-value {
          color: theme('colors.main');
          font-size: 14px;
          font-weight: 500;
        }
      }
    }

    &-destination-el {
      &-name {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 500;
      }

      border-bottom: 1px solid theme('colors.dark-background');
    }

    &-activity {
      &:nth-of-type(2n) {
        background-color: rgba(246, 248, 252, 1);
      }

      &:first-of-type {
        .order-step-info-side {
          padding-top: 12px;
        }

        .line-top {
          display: none;
        }
      }

      &:last-of-type {
        .line-bottom {
          display: none;
        }
      }

      .order-step-info {
        position: relative;

        &-date {
          color: rgba(39, 44, 63, 1);
          font-weight: 600;
          font-size: 14px;
        }

        &-side {
          .circle {
            height: 8px;
            width: 8px;
            background-color: rgba(255, 255, 255, 1);
            border: 2px solid rgba(125, 148, 231, 1);
            border-radius: 50%;
            left: -1rem;
          }

          .line-bottom {
            width: 1px;
            background-color: rgba(223, 226, 236, 1);
            border: 1px solid rgba(223, 226, 236, 1);
            height: 100%;
            top: 6px;
            left: 1.5px;
          }

          .line-top {
            width: 1px;
            background-color: rgba(223, 226, 236, 1);
            border: 1px solid rgba(223, 226, 236, 1);
            height: 12px;
            top: 6px;
            left: 1.5px;
          }
        }
      }

      .order-step-data {
        color: rgba(39, 44, 63, 1);
        font-weight: 400;
        font-size: 15px;
      }
    }
  }

  .roi {
    border-top: 1px solid theme('colors.dark-background');

    &-inputs-wrap:first-of-type {
      border-right: 1px solid theme('colors.dark-background');
    }

    &-results {
      background-color: rgba(246, 248, 252, 1);

      &-wrap {
        background-color: rgba(246, 248, 252, 1);

        &:first-of-type {
          border-right: 1px solid rgba(223, 226, 236, 1);
        }
      }

      &-label {
        color: rgba(82, 90, 122, 1);
        font-size: 16px;
        font-weight: 500;
      }

      &-value {
        color: rgba(39, 44, 63, 1);
        font-size: 16px;
        font-weight: 600;

        &-green {
          color: rgba(255, 255, 255, 1);
          background-color: rgba(11, 161, 125, 1);
          border-radius: 6px;
          padding: 6px 12px;
        }
      }
    }

    &-input {
      flex-direction: row;
      margin-bottom: 0 !important;
    }

    &-label {
      color: rgba(82, 90, 122, 1);
      font-size: 11px;
      font-weight: 500;
    }
  }

  .compliance-credit {
    &-confirmed {
      &-value {
        border-left: 4px solid rgba(98, 132, 254, 1);
        color: theme('colors.main');
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgba(98, 132, 254, 1);
        border-radius: 4px 0 0 4px;
      }
    }

    &-open {
      &-value {
        border-left: 4px solid rgba(243, 173, 43, 1);
        color: theme('colors.main');
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgba(243, 173, 43, 1);
      }
    }

    &-maximum {
      &-value {
        border-left: 4px dashed rgba(243, 173, 43, 1);
        color: theme('colors.main');
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background: repeating-linear-gradient(
          120deg,
          rgba(243, 173, 43, 1),
          rgba(243, 173, 43, 1) 1px,
          rgb(223, 243, 231) 0,
          rgb(223, 243, 231) 12px
        );
      }
    }

    &-remaining {
      &-value {
        border-left: 4px solid rgb(223, 243, 231);
        color: theme('colors.main');
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgb(223, 243, 231);
      }
    }

    &-overuse {
      &-value {
        border-left: 4px solid rgba(254, 98, 98, 0.12);
        color: rgba(254, 98, 98, 1);
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgba(254, 98, 98, 0.12);
        border-radius: 0 4px 4px 0;
      }
    }
  }
}
</style>
