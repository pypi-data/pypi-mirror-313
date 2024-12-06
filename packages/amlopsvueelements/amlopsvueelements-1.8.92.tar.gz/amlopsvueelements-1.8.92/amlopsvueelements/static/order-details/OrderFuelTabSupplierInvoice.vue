<template>
  <div class="w-full h-auto flex flex-col gap-2">
    <div
      v-for="(uplift, upliftIndex) in mockUplifts"
      :key="upliftIndex"
      class="supplier-invoice-step bg-white w-full border border-transparent rounded-md"
    >
      <div
        class="supplier-invoice-step-header flex justify-between items-center py-[1rem] px-[0.75rem]"
      >
        <div class="supplier-invoice-step-header-left flex gap-2">
          <div
            class="supplier-invoice-step-header-status"
            :class="{
              'supplier-invoice-step-header-status-confirmed': uplift.status === 'confirmed',
              'supplier-invoice-step-header-status-cancelled': uplift.status === 'cancelled'
            }"
          >
            <img
              v-if="uplift.status === 'confirmed'"
              width="12"
              height="12"
              src="../../assets/icons/check.svg"
              alt="approve"
            />
            <img
              v-else-if="uplift.status === 'cancelled'"
              width="12"
              height="12"
              src="../../assets/icons/status-close.svg"
              alt="delete"
            />
            <span v-else>{{ upliftIndex + 1 }}</span>
          </div>
          <div class="supplier-invoice-step-header-name">Uplift {{ upliftIndex + 1 }}</div>
        </div>

        <Button
          class="dropdown-button"
          @click="
            () => {
              uplift.is_shown = !uplift.is_shown;
            }
          "
          ><img
            :class="{ 'dropdown-button-open': uplift.is_shown }"
            src="../../assets/icons/chevron-down.svg"
            alt="hide"
        /></Button>
      </div>
      <div class="loading-wrap">
        <Loading v-if="isLoading" />
      </div>
      <div v-if="uplift && uplift.is_shown" class="supplier-invoice-step-content">
        <div class="supplier-invoice-step-content-header-big-wrap flex">
          <div class="supplier-invoice-step-content-header-big flex w-2/12"></div>
          <div class="supplier-invoice-step-content-header-big flex w-4/12 p-1">
            <div
              class="supplier-invoice-step-content-header-big-el flex w-full py-1 justify-center rounded"
            >
              Actual Supplier Pricing
            </div>
          </div>
          <div class="supplier-invoice-step-content-header-big flex w-4/12 p-1">
            <div
              class="supplier-invoice-step-content-header-big-el flex w-full py-1 justify-center rounded"
            >
              Actual Client Pricing
            </div>
          </div>
          <div class="supplier-invoice-step-content-header-big flex w-2/12"></div>
        </div>
        <div class="supplier-invoice-step-content-header-sub flex">
          <div
            class="supplier-invoice-step-content-header-sub-wrap flex w-2/12 py-[0.5rem] pl-[0.75rem] gap-2"
          >
            <div
              class="supplier-invoice-step-content-header-sub-el flex w-full justify-start el-border"
            >
              Item
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-header-sub-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]"
          >
            <div class="supplier-invoice-step-content-header-sub-el flex w-4/12 justify-start">
              Quantity
            </div>
            <div
              class="supplier-invoice-step-content-header-sub-el flex w-4/12 justify-start pl-[0.75rem]"
            >
              Unit Price
            </div>
            <div
              class="supplier-invoice-step-content-header-sub-el flex w-4/12 justify-start el-border"
            >
              Total Cost
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-header-sub-wrap flex w-4/12 p-[0.5rem] pl-[0.75rem]"
          >
            <div class="supplier-invoice-step-content-header-sub-el flex w-4/12 justify-start">
              Quantity
            </div>
            <div class="supplier-invoice-step-content-header-sub-el flex w-4/12 justify-start">
              Unit Price
            </div>
            <div
              class="supplier-invoice-step-content-header-sub-el flex w-4/12 justify-start el-border"
            >
              Total Cost
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-header-sub-wrap flex w-2/12 py-[0.5rem] pl-[0.75rem] gap-2"
          >
            <div class="supplier-invoice-step-content-header-sub-el flex w-full justify-start">
              Discrepancy
            </div>
          </div>
        </div>
        <div class="supplier-invoice-step-content-element flex">
          <div
            class="supplier-invoice-step-content-element-wrap flex w-2/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="supplier-invoice-step-content-element-el-name flex justify-start items-center w-8/12"
            >
              {{ orderStore?.order?.fuel_order?.fuel_category?.name }}
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light"
          >
            <div
              class="supplier-invoice-step-content-element-el flex justify-start items-center w-4/12"
            >
              {{ addThousandSeparators(orderStore?.order?.fuel_order?.fuel_quantity) }} ({{
                orderStore?.order?.fuel_order?.fuel_uom?.description_plural
              }})
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center"
            >
              <span class="text-light-subtitle pr-[0.5rem] text-[0.75rem]">x</span
              >{{ parseFloat(uplift?.fuel_pricing?.supplier?.unit_price_amount) }}
              {{ uplift?.fuel_pricing?.supplier?.unit_price_pricing_unit?.description_short }}
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center"
            >
              {{ formatNumber(uplift?.fuel_pricing?.supplier?.amount_total) }}
              {{ uplift?.fuel_pricing?.supplier?.amount_currency?.code }}
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]"
          >
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center pr-[0.5rem] pl-[1.75rem]"
            >
              <InputField
                :model-value="parseInt(uplift.fuel_pricing?.client?.quantity)"
                class="roi-input w-full"
                :is-white="true"
                placeholder=" "
                @update:model-value="
                  (value) => {
                    uplift.fuel_pricing.client.quantity = parseInt(value);
                  }
                "
              >
              </InputField>
              <span class="text-light-subtitle pl-[0.5rem] text-[0.75rem]">x</span>
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center"
            >
              <div class="input-wrap flex pr-[0.75rem]">
                <InputField
                  :model-value="removeTrailingZeros(uplift.fuel_pricing?.client?.unit_price_amount)"
                  class="w-6/12 mb-0"
                  :is-white="true"
                  :is-half="true"
                  placeholder=" "
                  @update:model-value="
                    (value) => {
                      uplift.fuel_pricing.client.unit_price_amount = value;
                    }
                  "
                />
                <SelectField
                  class="w-6/12 mb-0"
                  :is-white="true"
                  :is-half="true"
                  placeholder=" "
                  :options="[uplift.fuel_pricing?.client?.unit_price_pricing_unit]"
                  label="description_short"
                  :model-value="uplift.fuel_pricing?.client?.unit_price_pricing_unit"
                  :disabled="true"
                />
              </div>
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center pr-[0.75rem]"
            >
              <InputField
                :model-value="formatNumber(uplift.fuel_pricing?.client?.amount_total)"
                class="roi-input w-full"
                :is-white="true"
                placeholder=" "
                :disabled="true"
              >
                <template #suffix>{{
                  uplift.fuel_pricing?.client?.amount_currency?.code
                }}</template>
              </InputField>
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-element-wrap flex w-2/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              :class="{ 'discrepancy-red': uplift.fuel_pricing?.discrepancy?.amount_percent > 0 }"
              class="supplier-invoice-step-content-element-el-name flex justify-start items-center w-full discrepancy"
            >
              <span class="font-semibold pr-[0.25rem]">
                {{ addThousandSeparators(uplift.fuel_pricing?.discrepancy?.amount_total) }}
                {{ uplift.fuel_pricing?.discrepancy?.amount_currency?.code }}</span
              >
              <span class="font-normal"
                >({{ uplift.fuel_pricing?.discrepancy?.amount_percent }}%)</span
              >
            </div>
          </div>
        </div>
        <div
          v-if="uplift && uplift.fees?.length > 0"
          class="supplier-invoice-step-content-divider flex w-full py-[0.5rem] px-[0.75rem]"
        >
          Fees
        </div>
        <div
          v-for="(fee, key) in uplift.fees"
          v-if="uplift && uplift.fees.length > 0"
          :key="key"
          class="supplier-invoice-step-content-element flex"
        >
          <div
            class="supplier-invoice-step-content-element-wrap flex w-2/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="supplier-invoice-step-content-element-el-name flex justify-start items-center w-8/12"
            >
              {{
                fee.supplier?.suppliers_fuel_fees_rates_row?.supplier_fuel_fee?.fuel_fee_category
                  ?.name ?? 'Fee'
              }}
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light"
          >
            <div
              class="supplier-invoice-step-content-element-el flex justify-start items-center w-4/12"
            >
              {{ parseInt(fee.supplier?.quantity_value) }}
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center"
            >
              <span class="text-light-subtitle pr-[0.5rem] text-[0.75rem]">x</span>
              {{ formatNumber(parseFloat(fee.supplier?.unit_price_amount).toFixed(2)) }}
              {{ fee.supplier?.unit_price_pricing_unit?.description_short }}
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center"
            >
              {{ formatNumber(parseFloat(fee.supplier?.amount_total).toFixed(2)) }}
              {{ fee.supplier?.amount_currency?.code }}
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]"
          >
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center pr-[0.5rem]"
            >
              <CheckboxField v-model="fee.is_active" class="mb-0 pr-[0.75rem]" :size="'20px'" />
              <InputField
                v-if="fee.is_active"
                class="roi-input w-full"
                :model-value="parseInt(fee?.client?.quantity_value)"
                :is-white="true"
                placeholder=" "
                @update:model-value="
                  (value) => {
                    fee.client.quantity_value = parseInt(value);
                  }
                "
              >
              </InputField>
              <span v-else class="pl-[0.5rem] py-[0.7rem] w-full text-light-subtitle">--</span>
              <span class="text-light-subtitle pl-[0.5rem] text-[0.75rem]">x</span>
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center"
            >
              <div class="input-wrap flex pr-[0.75rem]">
                <InputField
                  v-if="fee.is_active"
                  :model-value="removeTrailingZeros(fee.client?.unit_price_amount)"
                  class="w-6/12 mb-0"
                  :is-white="true"
                  :is-half="true"
                  placeholder=" "
                  @update:model-value="
                    (value) => {
                      fee.client.unit_price_amount = value;
                    }
                  "
                />
                <SelectField
                  v-if="fee.is_active"
                  class="w-6/12 mb-0"
                  :is-white="true"
                  :is-half="true"
                  placeholder=" "
                  :options="[fee.client?.unit_price_pricing_unit]"
                  label="description_short"
                  :model-value="fee.client?.unit_price_pricing_unit"
                  :disabled="true"
                />
                <span
                  v-if="!fee.is_active"
                  class="pl-[0.5rem] py-[0.7rem] w-full text-light-subtitle"
                  >--</span
                >
              </div>
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center pr-[0.75rem]"
            >
              <InputField
                v-if="fee.is_active"
                class="roi-input w-full"
                :model-value="formatNumber(fee?.client?.amount_total)"
                :is-white="true"
                placeholder=" "
                :disabled="true"
              >
                <template #suffix>{{
                  fee?.client?.unit_price_pricing_unit?.currency?.code
                }}</template>
              </InputField>
              <span v-else class="pl-[0.5rem] py-[0.7rem] w-full text-light-subtitle">--</span>
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-element-wrap flex w-2/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              :class="{ 'discrepancy-red': fee?.discrepancy?.amount_percent > 0 }"
              class="supplier-invoice-step-content-element-el-name discrepancy flex justify-start items-center w-full"
            >
              <span class="font-semibold pr-[0.25rem]">
                {{ addThousandSeparators(fee.discrepancy?.amount_total) }}
                {{ fee.discrepancy?.amount_currency?.code }}</span
              >
              <span class="font-normal">({{ fee?.discrepancy?.amount_percent }}%)</span>
            </div>
          </div>
        </div>
        <div
          class="supplier-invoice-step-add flex cursor-pointer p-[0.75rem] gap-2 w-fit"
          @click="addFee(upliftIndex)"
        >
          <img src="../../assets/icons/plus.svg" alt="add" />
          Add Fee
        </div>
        <div
          v-if="uplift && uplift.taxes.length > 0"
          class="supplier-invoice-step-content-divider flex w-full py-[0.5rem] px-[0.75rem]"
        >
          Taxes
        </div>
        <div
          v-for="(tax, key) in uplift.taxes"
          v-if="uplift && uplift.taxes.length > 0"
          :key="key"
          class="supplier-invoice-step-content-element flex"
        >
          <div
            class="supplier-invoice-step-content-element-wrap flex w-2/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="supplier-invoice-step-content-element-el-name flex justify-start items-center w-full gap-1 relative"
            >
              {{ tax.supplier?.tax?.category?.name ?? 'Tax' }}
              <div
                class="supplier-invoice-step-content-block-body-note hover-wrap contents flex items-center"
              >
                <img
                  width="12"
                  height="12"
                  src="../../assets/icons/info-circle.svg"
                  alt="warn"
                  class="warn"
                />
                <div class="supplier-invoice-step-tooltip right-tooltip">
                  ● Applies on:
                  {{
                    tax.supplier.applies_on?.fuel
                      ? 'Fuel'
                      : tax.supplier.applies_on?.fees
                      ? Object.values(tax.supplier.applies_on?.fees)[0]
                      : tax.supplier.applies_on?.taxes
                      ? tax.supplier.applies_on?.taxes
                      : ''
                  }}
                </div>
              </div>
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light"
          >
            <div
              class="supplier-invoice-step-content-element-el flex justify-start items-center w-4/12"
            >
              &nbsp;
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center"
            >
              {{ tax?.supplier?.tax_percentage ? `${tax?.supplier?.tax_percentage}%` : '-' }}
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center"
            >
              {{ formatNumber(tax?.supplier?.tax_amount_total) }}
              {{ tax?.supplier?.tax_amount_currency?.code }}
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]"
          >
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center pr-[0.75rem]"
            >
              <CheckboxField v-model="tax.is_active" class="mb-0 pr-[0.75rem]" :size="'20px'" />
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center pr-[0.75rem]"
            >
              <InputField
                v-if="tax.is_active"
                class="roi-input w-full"
                :model-value="formatNumber(tax?.client?.tax_percentage)"
                :is-white="true"
                placeholder=" "
                :disabled="true"
              >
                <template #suffix>%</template>
              </InputField>
              <span v-else class="pl-[0.5rem] py-[0.7rem] w-full text-light-subtitle">--</span>
            </div>
            <div
              class="supplier-invoice-step-content-element-el flex w-4/12 justify-start items-center pr-[0.75rem]"
            >
              <InputField
                v-if="tax.is_active"
                class="roi-input w-full"
                :model-value="formatNumber(tax?.client?.tax_amount_total)"
                :is-white="true"
                placeholder=" "
                :disabled="true"
              >
                <template #suffix>{{ tax?.client?.tax_amount_currency?.code }}</template>
              </InputField>
              <span v-else class="pl-[0.5rem] py-[0.7rem] w-full text-light-subtitle">--</span>
            </div>
          </div>
          <div
            class="supplier-invoice-step-content-element-wrap flex w-2/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              :class="{ 'discrepancy-red': tax.discrepancy?.amount_percent > 0 }"
              class="supplier-invoice-step-content-element-el-name discrepancy flex justify-start items-center w-full"
            >
              <span class="font-semibold pr-[0.25rem]">
                {{ addThousandSeparators(tax.discrepancy?.amount_total) }}
                {{ tax.discrepancy?.amount_currency?.code }}</span
              >
              <span class="font-normal">({{ tax?.discrepancy?.amount_percent }}%)</span>
            </div>
          </div>
        </div>
        <div
          class="supplier-invoice-step-add flex cursor-pointer p-[0.75rem] gap-2 w-fit"
          @click="addTax(upliftIndex)"
        >
          <img src="../../assets/icons/plus.svg" alt="add" />
          Add Tax
        </div>
        <div class="supplier-invoice-step-content-results flex">
          <div class="supplier-invoice-step-content-results-wrap flex flex-col w-2/12">
            <div
              class="supplier-invoice-step-content-results-el-name flex items-center justify-center w-full p-[0.5rem] pl-[0.75rem] justify-start items-center"
            >
              &nbsp;
            </div>
            <div
              class="supplier-invoice-step-content-results-el-value flex w-full p-[0.5rem] justify-center items-center"
            >
              &nbsp;
            </div>
          </div>
          <div class="supplier-invoice-step-content-results-wrap flex flex-col w-4/12">
            <div
              class="supplier-invoice-step-content-results-el-name flex items-center justify-center w-full p-[0.5rem] pl-[0.75rem] justify-start items-center"
            >
              Calculated Supplier Price Total
            </div>
            <div
              class="supplier-invoice-step-content-results-el-value flex w-full p-[0.5rem] justify-center items-center"
            >
              {{ formatNumber(uplift?.pricing_summary?.supplier_total) }}
              {{ uplift.fuel_pricing?.supplier?.amount_currency?.code }}
            </div>
          </div>
          <div class="supplier-invoice-step-content-results-wrap flex flex-col w-4/12">
            <div
              class="supplier-invoice-step-content-results-el-name flex items-center justify-center w-full p-[0.5rem] pl-[0.75rem] justify-start items-center"
            >
              Actual Supplier Invoice Total
            </div>
            <div
              class="supplier-invoice-step-content-results-el-value flex w-full p-[0.5rem] justify-center items-center"
            >
              {{ formatNumber(uplift?.pricing_summary?.client_total) }}
              {{ uplift.fuel_pricing?.client?.amount_currency?.code }}
            </div>
          </div>
          <div class="supplier-invoice-step-content-results-wrap flex flex-col w-2/12">
            <div
              class="supplier-invoice-step-content-results-el-name flex items-center justify-start w-full p-[0.5rem] pl-[0.75rem] justify-start items-center"
            >
              Discrepancy Total
            </div>
            <div
              :class="{
                'discrepancy-red': uplift?.pricing_summary?.discrepancy?.amount_percent > 0
              }"
              class="supplier-invoice-step-content-results-el-value discrepancy flex w-full p-[0.5rem] justify-start items-center"
            >
              <span class="font-semibold pr-[0.25rem]">
                {{ formatNumber(uplift?.pricing_summary?.discrepancy?.amount_total) }}
                {{ uplift?.pricing_summary?.discrepancy?.amount_currency?.code }}
              </span>
              <span class="font-normal"
                >({{ uplift?.pricing_summary?.discrepancy?.amount_percent }}%)</span
              >
            </div>
          </div>
        </div>
        <div class="supplier-invoice-step-content-margin flex justify-end p-[0.75rem] gap-2">
          <Button
            class="approve-button cancel-button items-center gap-2"
            @click="
              () => {
                uplift.status = 'cancelled';
              }
            "
          >
            <img width="12" height="12" src="../../assets/icons/cross.svg" alt="delete" />
            Raise Supplier Dispute
          </Button>
          <Button
            class="approve-button approve-button-green flex items-center gap-3"
            @click="
              () => {
                uplift.status = 'confirmed';
              }
            "
          >
            <img src="../../assets/icons/check.svg" alt="approve" />
            Confirm as Reconciled
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type PropType, watch } from 'vue';
import { ref } from 'vue';
import { Button } from 'shared/components';
import { useOrderStore } from '@/stores/useOrderStore';
import { addThousandSeparators, formatNumber, removeTrailingZeros } from '@/helpers/order';
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

const mockUplift = {
  status: null,
  is_shown: true,
  fuel_pricing: {
    supplier: {
      unit_price_amount: '100',
      unit_price_pricing_unit: { description_short: 'USD/G' },
      amount_total: '500',
      amount_currency: { code: 'USD' }
    },
    client: {
      quantity: 500,
      unit_price_amount: '110',
      amount_total: '550',
      unit_price_pricing_unit: { description_short: 'USD/G' },
      amount_currency: { code: 'USD' }
    },
    discrepancy: {
      amount_total: '550',
      amount_currency: { code: 'USD' },
      amount_percent: 6.21
    }
  },
  fees: [
    {
      supplier: {
        suppliers_fuel_fees_rates_row: {
          supplier_fuel_fee: { fuel_fee_category: { name: 'Environmental Fee' } }
        },
        quantity_value: 5,
        unit_price_amount: '20',
        unit_price_pricing_unit: { description_short: 'USD' },
        amount_total: '100',
        amount_currency: { code: 'USD' },
        is_active: true
      },
      client: {
        quantity_value: 5,
        unit_price_amount: '22',
        amount_total: '110',
        unit_price_pricing_unit: { description_short: 'USD' }
      },
      discrepancy: {
        amount_total: '550',
        amount_currency: { code: 'USD' },
        amount_percent: 6.21
      }
    }
  ],
  taxes: [
    {
      supplier: {
        tax: { category: { name: 'VAT' } },
        tax_percentage: 10,
        tax_amount_total: '50',
        tax_amount_currency: { code: 'USD' },
        applies_on: { fuel: true }
      },
      client: {
        is_active: true,
        tax_percentage: 10,
        tax_amount_total: '55',
        tax_amount_currency: { code: 'USD' }
      },
      discrepancy: {
        amount_total: '550',
        amount_currency: { code: 'USD' },
        amount_percent: -6.21
      }
    }
  ],
  pricing_summary: {
    supplier_total: 650,
    client_total: 715,
    margin_amount: 65,
    margin_percentage: 10,
    discrepancy: {
      amount_total: '550',
      amount_currency: { code: 'USD' },
      amount_percent: 6.21
    }
  }
};

const mockUplifts: any = ref([
  mockUplift,
  JSON.parse(JSON.stringify({ ...mockUplift, status: 'confirmed', is_shown: false })),
  JSON.parse(JSON.stringify({ ...mockUplift, status: 'cancelled', is_shown: false }))
]);

const orderStore = useOrderStore();

const addFee = (upliftId: number) => {
  mockUplifts.value?.[upliftId].fees?.push({
    supplier: {
      suppliers_fuel_fees_rates_row: {
        supplier_fuel_fee: { fuel_fee_category: { name: '' } }
      },
      quantity_value: 1,
      unit_price_amount: '0',
      unit_price_pricing_unit: { description_short: '' },
      amount_total: '0',
      amount_currency: { code: 'USD' },
      is_active: true
    },
    client: {
      quantity_value: 1,
      unit_price_amount: '0',
      amount_total: '0',
      unit_price_pricing_unit: { description_short: 'USD' }
    },
    discrepancy: {
      amount_total: '0',
      amount_currency: { code: 'USD' },
      amount_percent: 0
    }
  });
};

const addTax = (upliftId: number) => {
  mockUplifts.value?.[upliftId].taxes?.push({
    supplier: {
      tax: { category: { name: '' } },
      tax_percentage: 0,
      tax_amount_total: '0',
      tax_amount_currency: { code: 'USD' }
    },
    client: {
      is_active: true,
      tax_percentage: 0,
      tax_amount_total: '0',
      tax_amount_currency: { code: 'USD' }
    },
    discrepancy: {
      amount_total: '0',
      amount_currency: { code: 'USD' },
      amount_percent: 0
    }
  });
};

watch(
  () => props.order,
  async (order: IOrder) => {
    if (order?.type?.is_fuel) {
      // TO DO: Add fetchers
    }
  }
);
</script>

<style lang="scss">
.supplier-invoice-step {
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

  .approve-button {
    background-color: rgba(240, 242, 252, 1) !important;
    color: rgba(81, 93, 138, 1) !important;
    border-color: transparent !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-[0.5rem] px-[1rem] rounded-lg #{!important};

    &-green {
      background-color: rgba(11, 161, 125, 1) !important;
      color: rgba(255, 255, 255, 1) !important;

      img {
        filter: brightness(0) saturate(100%) invert(100%) sepia(100%) saturate(0%)
          hue-rotate(251deg) brightness(102%) contrast(103%);
      }
    }

    &:disabled {
      background-color: rgba(139, 148, 178, 0.12) !important;
      color: rgb(139, 148, 178) !important;
    }
  }

  .cancel-button {
    background-color: rgba(254, 98, 98, 0.12) !important;
    color: rgba(254, 98, 98, 1) !important;

    img {
      filter: brightness(0) saturate(100%) invert(71%) sepia(81%) saturate(4491%) hue-rotate(321deg)
        brightness(100%) contrast(108%);
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
      .supplier-invoice-step-tooltip {
        display: block;
      }
    }
  }

  &-add {
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

      &-confirmed {
        background-color: rgba(11, 161, 125, 0.12);
      }

      &-cancelled {
        background-color: rgba(254, 98, 98, 1);
      }
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
        background-color: rgba(255, 255, 255, 1) !important;

        .supplier-invoice-step-content-col-data {
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
      border-bottom: 1px solid rgba(239, 241, 246, 1);

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

    .discrepancy {
      color: rgba(11, 161, 125, 1);
      &-red {
        color: rgba(221, 44, 65, 1);
      }
    }

    &-results {
      &-wrap {
        border-left: 1px solid rgb(223, 226, 236);
        border-bottom: 1px solid rgb(223, 226, 236);
      }

      &-el {
        &-name {
          background-color: rgba(246, 248, 252, 1);
          color: rgba(82, 90, 122, 1);
          font-size: 11px;
          font-weight: 500;
        }

        &-value {
          color: rgba(39, 44, 63, 1);
          font-size: 16px;
          font-weight: 600;
        }
      }
    }

    &-divider {
      text-transform: uppercase;
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
