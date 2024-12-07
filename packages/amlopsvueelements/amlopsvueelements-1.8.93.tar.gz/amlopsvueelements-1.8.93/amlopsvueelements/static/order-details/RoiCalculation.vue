<template>
  <div class="pricing-step bg-white w-full border border-transparent rounded-md">
    <div class="pricing-step-header flex justify-between py-[1rem] px-[0.75rem]">
      <div class="pricing-step-header-name">
        {{ order?.fuel_order?.is_open_release ? 'Indicative' : '' }} ROI Calculation
        {{ upliftPricingObj ? ' - Actual Uplift(s)' : '' }}
      </div>
      <div class="loading-wrap">
        <Loading v-if="isLoadingUpdateOrderRoi" />
      </div>
    </div>
    <div
      v-if="orderPricing && order && orderPricing.supplier_id"
      class="pricing-step-content roi flex flex-col"
    >
      <div class="roi-inputs flex">
        <div class="roi-inputs-wrap w-6/12 flex items-center p-3">
          <div class="roi-label w-6/12">Supplier Credit Terms</div>
          <InputField
            class="roi-input w-6/12"
            :is-white="true"
            placeholder=" "
            :disabled="true"
            :model-value="orderRoiDays?.supplier_terms_days"
            @update:model-value="emit('update:roi', $event, false, upliftPricingObj)"
          >
            <template #suffix>days</template>
          </InputField>
        </div>
        <div class="roi-inputs-wrap w-6/12 flex items-center p-3">
          <div class="roi-label w-6/12">Client Credit Terms</div>
          <InputField
            class="roi-input w-6/12"
            :is-white="true"
            placeholder=" "
            :disabled="isDisabled"
            :model-value="orderRoiDays?.client_terms_days"
            @update:model-value="emit('update:roi', $event, true, upliftPricingObj)"
          >
            <template #suffix>days</template>
          </InputField>
        </div>
      </div>
      <div class="roi-results flex py-[0.75rem]">
        <div class="roi-results-wrap w-6/12 flex items-center px-[0.75rem]">
          <div class="roi-results-label w-6/12">Order Value</div>
          <div class="roi-results-value flex gap-2 w-6/12">
            {{ formatNumber(orderRoi?.calculated_roi_value) }} USD
            <div
              v-if="
                orderRoi?.calculated_roi_value_order_currency &&
                orderPricing?.fuel_pricing?.client?.amount_currency?.code !== 'USD'
              "
              class="font-medium"
            >
              ({{ orderRoi?.calculated_roi_value_order_currency }}
              {{ orderPricing?.fuel_pricing?.client?.amount_currency?.code }})
            </div>
          </div>
        </div>
        <div class="roi-results-wrap w-6/12 flex items-center px-[0.75rem]">
          <div class="roi-results-label w-6/12">ROI</div>
          <div class="roi-results-value-green" :style="roiStyle">
            {{
              orderRoi?.calculated_roi === '1000000.00'
                ? 'Ꝏ'
                : formatNumber(orderRoi?.calculated_roi)
            }}
            %
          </div>
        </div>
      </div>
    </div>
    <div v-else class="pricing-step-content-missing flex items-center justify-center py-[1.25rem]">
      <Loading v-if="props.isLoading" />
      <span v-else>Please select a Fuel Supply option</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PropType } from 'vue';
import { formatNumber } from '@/helpers/order';
import { getRoiStyle } from '@/helpers/roi';
import InputField from '../forms/fields/InputField.vue';
import Loading from '../forms/Loading.vue';

import type {
  IFuelPricingObj,
  IOrder,
  IOrderRoi,
  IRoiDays,
  IUpliftFuelPricingObj
} from 'shared/types';

const props = defineProps({
  order: {
    type: Object as PropType<IOrder | null>,
    default: null
  },
  orderRoi: {
    type: Object as PropType<IOrderRoi | null>,
    default: null
  },
  orderPricing: {
    type: Object as PropType<IFuelPricingObj | null>,
    default: null
  },
  orderRoiDays: {
    type: Object as PropType<IRoiDays | null>,
    default: null
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  isDisabled: {
    type: Boolean,
    default: false
  },
  isLoadingUpdateOrderRoi: {
    type: Boolean,
    default: false
  },
  upliftPricingObj: {
    type: Object as PropType<IUpliftFuelPricingObj | null>,
    default: () => null
  }
});

type Emits = {
  (
    e: 'update:roi',
    days: string,
    isClient: boolean,
    upliftPricingObj: IUpliftFuelPricingObj | null
  ): void;
};

const emit = defineEmits<Emits>();

const roiStyle = computed(() => getRoiStyle(props.orderRoi));
</script>
