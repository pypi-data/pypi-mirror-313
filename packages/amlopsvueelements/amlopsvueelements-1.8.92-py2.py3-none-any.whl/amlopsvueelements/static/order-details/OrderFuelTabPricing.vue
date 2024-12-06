<template>
  <div class="w-full h-auto flex flex-col gap-2">
    <SupplyFuelDetailsModal
      v-if="supplyFuel"
      ref="clientInput"
      :is-open="isModalOpened"
      :supply-fuel="supplyFuel"
      :result-index="selectedModalSupplier!"
      :is-open-release="order?.type.is_fuel && order?.fuel_order?.is_open_release"
      name="order-modal"
      @modal-close="closeModal"
    />
    <div class="pricing-step bg-white w-full border border-transparent rounded-md">
      <div class="pricing-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="pricing-step-header-name">Select Supplier Fuel</div>
      </div>
      <div
        v-if="!!supplyFuel?.results?.length && !isLoadingSupplyFuel && !isLoadingOrderPricing"
        class="pricing-step-content w-full flex flex-col"
      >
        <div class="pricing-step-content-header-wrap w-full flex items-center">
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">Fuel</div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">Supplier</div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">IPA</div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">Delivery</div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">Apron</div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">Terminal</div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">
              Total Uplift Cost
            </div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">&nbsp;</div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">&nbsp;</div>
          </div>
        </div>
        <div
          v-for="(supplier, index) in supplyFuel?.results"
          :key="index"
          class="pricing-step-content-data-wrap w-full flex items-center"
          :class="{ 'selected-supplier': selectedSupplierIndex === index }"
          :style="{
            background:
              supplier.color && selectedSupplierIndex === null
                ? `${changeColorAlpha(supplier.color, 0.1)}`
                : 'rgba(246, 248, 252, 0.5)'
          }"
        >
          <div class="pricing-step-content-col w-1/12">
            <div
              class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem] flex gap-2 items-center"
            >
              <div
                class="pricing-step-content-col-data-indicator"
                :style="{
                  background: supplier.color
                }"
              ></div>
              <span>{{ supplier.fuel_type.name }}</span>
            </div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ supplier.supplier.full_repr }}
            </div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{
                supplier.ipa?.full_repr
                  ? supplier.ipa?.full_repr
                  : selectedSupplierIndex !== null
                  ? '-'
                  : 'TBC'
              }}
            </div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ supplier.delivery_method?.name ?? 'All' }}
            </div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ supplier.apron?.name ?? 'All' }}
            </div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ supplier.terminal?.name ?? 'All' }}
            </div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ formatNumber(supplier.total_uplift_cost) }} {{ supplier.currency.code }}
            </div>
          </div>
          <div class="pricing-step-content-col w-1/12 relative">
            <div
              class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem] flex justify-end gap-2"
            >
              <div v-if="supplier.issues.length > 0" class="hover-wrap contents">
                <img
                  width="20"
                  height="20"
                  src="../../assets/icons/alert.svg"
                  alt="warn"
                  class="warn"
                />
                <div class="pricing-step-tooltip">
                  <div
                    v-for="(issue, issueId) in supplier.issues"
                    :key="issueId"
                    v-html="'● ' + issue"
                  ></div>
                </div>
              </div>
              <img
                width="20"
                height="20"
                src="../../assets/icons/eye.svg"
                alt="details"
                class="cursor-pointer"
                @click="openModal(index)"
              />
            </div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem] flex justify-center">
              <Button
                v-if="selectedSupplierIndex === null"
                :disabled="supplier.is_expired || isSelectingSupplier"
                class="button"
                @click="selectSupplier(index, supplier)"
                >Select</Button
              >
              <div
                v-else
                class="selection-tick flex items-center justify-center"
                @click="selectSupplier(null, supplier)"
              >
                <img width="20" height="20" src="../../assets/icons/check.svg" alt="check" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-if="supplyFuel?.results?.length === 0 && !isLoadingSupplyFuel"
        class="pricing-step-content-none w-full flex py-[1rem] pr-[0.75rem] pl-[2.5rem] flex flex-col"
      >
        <img width="20" height="20" src="../../assets/icons/alert.svg" alt="warn" class="warn" />
        <div class="pricing-step-content-none-header">
          There are no supplier fuel supply options available at this location
        </div>
        <div class="pricing-step-content-none-desc">
          Please update the database with at least one supply option for this location and then
          revisit this page to proceed with the order.
        </div>
      </div>
      <div
        v-if="isLoadingSupplyFuel"
        class="pricing-step-content w-full flex py-8 px-[0.75rem] flex flex-col"
      >
        <Loading />
      </div>
    </div>
    <FuelPricingDetails
      :order="props.order"
      :is-loading="isLoadingOrderPricing"
      :is-loading-update-order-pricing="isLoadingUpdateOrderPricing"
    />
    <RoiCalculation
      :order="props.order"
      :order-roi="orderRoi"
      :order-roi-days="orderRoiDays"
      :order-pricing="orderPricing"
      :is-loading="isLoadingOrderPricing"
      :is-loading-update-order-roi="isLoadingUpdateOrderRoi"
      @update:roi="onRoiChange"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, type PropType, type Ref, ref, watch } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { storeToRefs } from 'pinia';
import { Button } from 'shared/components';
import { useFetch } from 'shared/composables';
import { useOrderReferenceStore } from '@/stores/useOrderReferenceStore';
import { useOrderStore } from '@/stores/useOrderStore';
import OrderReferences from '@/services/order/order-references';
import { changeColorAlpha } from '@/helpers/colors';
import { formatNumber } from '@/helpers/order';
import FuelPricingDetails from '../datacomponent/FuelPricingDetails.vue';
import RoiCalculation from '../datacomponent/RoiCalculation.vue';
import Loading from '../forms/Loading.vue';
import SupplyFuelDetailsModal from '../modals/SupplyFuelDetailsModal.vue';

import type { IFuelPricingObj, IOrder } from 'shared/types';

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
const isCurrentStep = computed(
  () => orderStore.currentStep === 1 && orderStore.order?.type?.is_fuel
);
const orderReferenceStore = useOrderReferenceStore();
const queryClient = useQueryClient();

const { fetchOrderPricing, onRoiChange, onSelectSupplier } = orderReferenceStore;

const {
  isLoadingOrderPricing,
  isLoadingSupplyFuel,
  isLoadingUpdateOrderPricing,
  isLoadingUpdateOrderRoi,
  orderPricing,
  orderRoi,
  orderRoiDays,
  selectedSupplierIndex,
  supplyFuel
} = storeToRefs(orderReferenceStore);
const isSelectingSupplier = ref(false);
const isRoiUpdatedOnLoad = ref(false);

const selectSupplier = async (id: number | null, supplier: any) => {
  if (id !== null && supplyFuel.value) {
    isSelectingSupplier.value = true;
    const data = await selectFuelSupplier(props.order.id!, {
      id: supplyFuel.value.id,
      key: parseInt(supplier.key!)
    });
    isSelectingSupplier.value = false;
    if (data) {
      selectedSupplierIndex.value = id;
      queryClient.invalidateQueries({ queryKey: ['orderStatus', props.order.id] });
      onSelectSupplier({
        supplierId: supplyFuel.value?.id,
        detailsId: Number(supplyFuel.value?.results[id]?.key)
      });
    }
  }
};

const isModalOpened = ref(false);
const selectedModalSupplier: Ref<null | number> = ref(null);

const openModal = (id: number) => {
  selectedModalSupplier.value = id;
  isModalOpened.value = true;
};

const closeModal = () => {
  selectedModalSupplier.value = null;
  isModalOpened.value = false;
};

const { callFetch: selectFuelSupplier } = useFetch<any>(
  async (orderId: number, payload: { id: number; key: number }) => {
    const data = await OrderReferences.selectFuelSupplier(orderId, payload);
    await fetchOrderPricing(props.order.id!);
    await orderReferenceStore.initiateReferenceStore(
      props.order.id!,
      props.order.pricing_calculation_record
    );
    await orderStore.fetchOrder(props.order.id!);
    return data;
  }
);

watch(
  () => props.order,
  async (order: IOrder) => {
    if (order?.type?.is_fuel) {
      Promise.allSettled([fetchOrderPricing(order.id!)]);
    }
  }
);

watch(
  () => [isCurrentStep.value, orderPricing.value],
  ([step, pricing]) => {
    if (step && pricing && !isRoiUpdatedOnLoad.value) {
      onRoiChange(
        (pricing as IFuelPricingObj)?.terms_days?.client_terms_days?.toString() ?? '0',
        true
      );
      isRoiUpdatedOnLoad.value = true;
    }
  }
);
</script>

<style lang="scss">
.pricing-step {
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
  }

  .dropdown-button {
    background-color: rgba(240, 242, 252, 1) !important;
    color: rgba(81, 93, 138, 1) !important;
    border-color: transparent !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-[0.5rem] rounded-xl #{!important};

    &-open {
      transform: rotate(180deg);
    }
  }

  .el-border {
    border-right: 1px solid rgb(223, 226, 236);

    &-light {
      border-right: 1px solid theme('colors.dark-background');
    }
  }

  .hover-wrap {
    &:hover {
      .pricing-step-tooltip {
        display: block;
      }
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

    &-status {
      background-color: rgba(240, 242, 252, 1);
      color: rgba(81, 93, 138, 1);
      width: 24px;
      height: 24px;
      line-height: 24px;
      border-radius: 50%;
      display: flex;
      font-size: 11px;
      font-weight: 600;
      justify-content: center;
    }
  }

  &-content {
    &-data-wrap {
      border-bottom: 1px solid theme('colors.dark-background');
      background-color: rgba(246, 248, 252, 0.5);

      &:last-of-type {
        border-radius: 0 0 8px 8px;
      }

      &.selected-supplier {
        background: #f1faf7 !important;

        .pricing-step-content-col-data {
          color: rgba(39, 44, 63, 1);
          background-color: #f1faf7;

          .warn {
            filter: none;
          }

          .selection-tick {
            display: flex;
            border-radius: 12px;
            background-color: rgba(11, 161, 125, 1);
            height: 40px;
            width: 40px;

            img {
              filter: brightness(0) saturate(100%) invert(97%) sepia(15%) saturate(264%)
                hue-rotate(204deg) brightness(122%) contrast(100%);
            }
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

        &-indicator {
          width: 4px;
          min-width: 4px;
          height: 24px;
          border-radius: 2px;
        }

        .warn {
          filter: brightness(0) saturate(100%) invert(89%) sepia(7%) saturate(740%)
            hue-rotate(193deg) brightness(88%) contrast(92%);
        }

        .selection-tick {
          display: none;
        }

        .files-button {
          border: 1px solid rgba(223, 226, 236, 1);
          border-radius: 6px;
        }

        .horizontal {
          transform: rotate(90deg);
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
}
</style>
