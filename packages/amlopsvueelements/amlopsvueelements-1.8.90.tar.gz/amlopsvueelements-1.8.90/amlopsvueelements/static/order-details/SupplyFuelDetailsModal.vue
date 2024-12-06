<template>
  <div v-if="isOpen" class="order-modal supply-fuel-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-header flex justify-between">
          Supplier Fuel Pricing Details
          <img
            width="12"
            height="12"
            src="../../assets/icons/cross.svg"
            alt="delete"
            class="close cursor-pointer"
            @click="emit('modal-close')"
          />
        </div>
        <div
          v-if="isLoadingSupplierFuelDetails"
          class="py-[1.5rem] px-[0.75rem] min-h-[70vh] flex items-center"
        >
          <Loading></Loading>
        </div>
        <ScrollBar v-else class="my-0">
          <div class="order-modal-body">
            <div class="order-modal-body-header flex gap-4">
              <div class="order-modal-body-header-col w-6/12 flex flex-col gap-2">
                <div class="order-modal-body-header-el flex gap-2">
                  <div class="order-modal-body-header-el-name w-6/12">Location</div>
                  <div class="order-modal-body-header-el-data w-6/12">
                    {{ supplyFuelDetails?.airport?.full_repr ?? '--' }}
                  </div>
                </div>
                <div class="order-modal-body-header-el flex gap-2">
                  <div class="order-modal-body-header-el-name w-6/12">Into-Plane Agent</div>
                  <div class="order-modal-body-header-el-data w-6/12">
                    {{ supplyFuelDetails?.ipa?.full_repr ?? '--' }}
                  </div>
                </div>
                <div class="order-modal-body-header-el flex gap-2">
                  <div class="order-modal-body-header-el-name w-6/12">Pricing Type</div>
                  <div class="order-modal-body-header-el-data w-6/12">
                    <div v-if="!supplyFuelDetails?.fuel_price?.pricing_link">{{ '--' }}</div>
                    <div v-else v-html="supplyFuelDetails?.fuel_price?.pricing_link"></div>
                  </div>
                </div>
                <div class="order-modal-body-header-el flex gap-2">
                  <div class="order-modal-body-header-el-name w-6/12">Handler-Specific Pricing</div>
                  <div class="order-modal-body-header-el-data w-6/12">
                    {{
                      supplyFuelDetails?.handler_specific_pricing
                        ? supplyFuelDetails?.handler_specific_pricing?.name
                        : 'No'
                    }}
                  </div>
                </div>
                <div class="order-modal-body-header-el flex gap-2">
                  <div class="order-modal-body-header-el-name w-6/12">Apron-Specific Pricing</div>
                  <div class="order-modal-body-header-el-data w-6/12">
                    {{
                      supplyFuelDetails?.apron_specific_pricing
                        ? supplyFuelDetails?.apron_specific_pricing?.name
                        : 'No'
                    }}
                  </div>
                </div>
              </div>
              <div class="order-modal-body-header-col w-6/12 flex flex-col gap-2">
                <div class="order-modal-body-header-el flex gap-2">
                  <div class="order-modal-body-header-el-name w-6/12">Supplier</div>
                  <div class="order-modal-body-header-el-data w-6/12">
                    {{ supplyFuelDetails?.supplier?.full_repr ?? '--' }}
                  </div>
                </div>
                <div class="order-modal-body-header-el flex gap-2">
                  <div class="order-modal-body-header-el-name w-6/12">Intermediate Supplier</div>
                  <div class="order-modal-body-header-el-data w-6/12">
                    {{
                      supplyFuelDetails?.intermediate_supplier
                        ? supplyFuelDetails?.intermediate_supplier?.full_repr
                        : 'No'
                    }}
                  </div>
                </div>
                <div class="order-modal-body-header-el flex gap-2">
                  <div class="order-modal-body-header-el-name w-6/12">Delivery Method</div>
                  <div class="order-modal-body-header-el-data w-6/12">
                    {{
                      supplyFuelDetails?.delivery_method
                        ? supplyFuelDetails?.delivery_method.name
                        : 'TBC'
                    }}
                  </div>
                </div>
                <div class="order-modal-body-header-el flex gap-2">
                  <div class="order-modal-body-header-el-name w-6/12">Client-Specific Pricing</div>
                  <div class="order-modal-body-header-el-data w-6/12">
                    {{
                      supplyFuelDetails?.client_specific_pricing
                        ? supplyFuelDetails?.client_specific_pricing?.name
                        : 'No'
                    }}
                  </div>
                </div>
                <div class="order-modal-body-header-el flex gap-2">
                  <div class="order-modal-body-header-el-name w-6/12">
                    Terminal-Specific Pricing
                  </div>
                  <div class="order-modal-body-header-el-data w-6/12">
                    {{
                      supplyFuelDetails?.terminal_specific_pricing
                        ? supplyFuelDetails?.terminal_specific_pricing?.name
                        : 'No'
                    }}
                  </div>
                </div>
              </div>
            </div>
            <div class="order-modal-body-content-wrap flex">
              <div class="order-modal-body-content w-full flex flex-col gap-2">
                <div
                  v-if="supplyFuelDetails?.issues && supplyFuelDetails?.issues.length > 0"
                  class="order-modal-body-content-block"
                >
                  <div class="order-modal-body-content-block-header issues p-[0.75rem]">
                    <img
                      width="20"
                      height="20"
                      src="../../assets/icons/alert.svg"
                      alt="warn"
                      class="warn"
                    />
                    {{
                      props.isOpenRelease && supplyFuelDetails
                        ? supplyFuelDetails?.issues.length + 1
                        : supplyFuelDetails?.issues.length
                    }}
                    {{
                      (props.isOpenRelease && supplyFuelDetails.issues.length >= 1) ||
                      supplyFuelDetails?.issues.length >= 2
                        ? 'Issues'
                        : 'Issue'
                    }}
                    Detected
                  </div>
                  <div
                    class="order-modal-body-content-block-body px-[0.75rem] py-[1rem] pl-[1.5rem] gap-3 flex flex-col"
                  >
                    <div v-if="props.isOpenRelease" class="issue-html">
                      This is an open fuel release, and as such an indicative fuel quantity is used.
                      Additionally, as the destination is not known, the flight destination for the
                      order is treated as domestic to represent the worst-case exposure scenario.
                    </div>
                    <div
                      v-for="(issue, issueId) in supplyFuelDetails?.issues"
                      :key="issueId"
                      class="issue-html"
                      v-html="issue"
                    ></div>
                  </div>
                </div>
                <div class="order-modal-body-content-block">
                  <div class="order-modal-body-content-block-header p-[0.75rem]">Fuel Pricing</div>
                  <div class="order-modal-body-content-block-body flex px-[0.75rem] py-[1rem]">
                    <div class="order-modal-body-content-block-body-name w-4/12">
                      {{ supplyFuelDetails?.fuel_price?.fuel?.name }}
                    </div>
                    <div
                      class="order-modal-body-content-block-body-desc w-6/12 relative flex items-center gap-2"
                    >
                      {{ supplyFuelDetails?.fuel_price?.unit_price }}
                      {{ supplyFuelDetails?.fuel_price?.pricing_unit?.description }} X
                      {{ addThousandSeparators(supplyFuel.scenario.uplift_qty) }}
                      {{ supplyFuel?.scenario.uplift_uom?.description_plural }}
                      <div
                        class="order-modal-body-content-block-body-note hover-wrap contents flex items-center"
                      >
                        <img
                          width="12"
                          height="12"
                          src="../../assets/icons/info-circle.svg"
                          alt="warn"
                          class="warn"
                        />
                        <div class="order-modal-body-tooltip left-tooltip">
                          <div
                            v-for="(note, noteId) in supplyFuelDetails?.fuel_price?.notes"
                            :key="noteId"
                            v-html="'● ' + note"
                          ></div>
                        </div>
                      </div>
                    </div>
                    <div class="order-modal-body-content-block-body-value w-2/12">
                      {{ formatNumber(supplyFuelDetails?.fuel_price?.amount) }}
                      {{ supplyFuelDetails?.currency?.code }}
                    </div>
                  </div>
                </div>
                <div class="order-modal-body-content-block">
                  <div class="order-modal-body-content-block-header p-[0.75rem]">Fees</div>
                  <div
                    v-if="
                      supplyFuelDetails &&
                      (Object.keys(supplyFuelDetails?.fees?.list).length === 0 ||
                        !supplyFuelDetails.hasOwnProperty('fees'))
                    "
                    class="results order-modal-body-content-block-body flex px-[0.75rem] py-6 flex justify-center border border-transparent rounded"
                  >
                    <div
                      class="order-modal-body-content-block-body-name flex flex-col items-center"
                    >
                      No fees calculated for this scenario
                    </div>
                  </div>
                  <div
                    v-for="(fee, key) in supplyFuelDetails?.fees?.list"
                    v-else
                    :key="key"
                    class="order-modal-body-content-block-body flex px-[0.75rem] py-[1rem]"
                  >
                    <div class="order-modal-body-content-block-body-name w-4/12">
                      {{ fee.display_name ?? 'Custom Fee' }}
                      <div
                        class="order-modal-body-content-block-body-note hover-wrap contents flex items-center"
                      >
                        <img
                          width="12"
                          height="12"
                          src="../../assets/icons/info-circle.svg"
                          alt="warn"
                          class="warn"
                        />
                        <div class="order-modal-body-tooltip">
                          <div
                            v-for="(note, noteId) in fee.notes"
                            :key="noteId"
                            v-html="'● ' + note"
                          ></div>
                        </div>
                      </div>
                    </div>
                    <div class="order-modal-body-content-block-body-desc w-6/12"></div>
                    <div class="order-modal-body-content-block-body-value w-2/12">
                      {{ formatNumber(fee?.amount) }} {{ supplyFuelDetails?.currency?.code }}
                    </div>
                  </div>
                </div>
                <div class="order-modal-body-content-block">
                  <div class="order-modal-body-content-block-header p-[0.75rem]">Taxes</div>
                  <div
                    v-if="
                      supplyFuelDetails &&
                      (Object.keys(supplyFuelDetails?.taxes?.list).length === 0 ||
                        !supplyFuelDetails.hasOwnProperty('taxes'))
                    "
                    class="results order-modal-body-content-block-body flex px-[0.75rem] py-6 flex justify-center border border-transparent rounded"
                  >
                    <div
                      class="order-modal-body-content-block-body-name flex flex-col items-center"
                    >
                      No taxes calculated for this scenario
                    </div>
                  </div>
                  <div v-else class="order-modal-body-content-block-body flex flex-col">
                    <div class="flex w-full">
                      <div class="order-modal-body-content-block-body-header w-6/12 text-center">
                        <div
                          class="el-border order-modal-body-content-block-body-header-el my-[0.5rem]"
                        >
                          Official Taxes
                        </div>
                      </div>
                      <div class="order-modal-body-content-block-body-header w-6/12 text-center">
                        <div class="order-modal-body-content-block-body-header-el my-[0.5rem]">
                          Supplier-Defined Taxes
                        </div>
                      </div>
                    </div>
                    <div
                      v-for="(tax, key) in supplyFuelDetails?.taxes?.list"
                      :key="key"
                      class="flex w-full"
                    >
                      <div
                        class="el-border w-6/12 issues flex px-[0.75rem] py-[1rem] items-center relative"
                      >
                        <div class="order-modal-body-content-block-body-name w-8/12">
                          {{ key }}
                          <div
                            v-if="tax.official.tax_notes.length"
                            class="order-modal-body-content-block-body-note hover-wrap contents flex items-center"
                          >
                            <img
                              width="12"
                              height="12"
                              src="../../assets/icons/info-circle.svg"
                              alt="warn"
                              class="warn"
                            />
                            <div class="order-modal-body-tooltip">
                              <div
                                v-for="(note, noteId) in tax.official.tax_notes"
                                :key="noteId"
                                v-html="'● ' + note"
                              ></div>
                            </div>
                          </div>
                        </div>
                        <div class="order-modal-body-content-block-body-value w-4/12">
                          {{ formatNumber(tax?.official?.amount) }}
                          {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                      <div class="w-6/12 issues flex px-[0.75rem] py-[1rem] items-center relative">
                        <div class="order-modal-body-content-block-body-name w-8/12">
                          {{ key }}
                          <div
                            v-if="tax.supplier.tax_notes.length"
                            class="order-modal-body-content-block-body-note hover-wrap contents flex items-center"
                          >
                            <img
                              width="12"
                              height="12"
                              src="../../assets/icons/info-circle.svg"
                              alt="warn"
                              class="warn"
                            />
                            <div class="order-modal-body-tooltip left-tooltip">
                              <div
                                v-for="(note, noteId) in tax.supplier.tax_notes"
                                :key="noteId"
                                v-html="'● ' + note"
                              ></div>
                            </div>
                          </div>
                        </div>
                        <div class="order-modal-body-content-block-body-value w-4/12">
                          {{ formatNumber(tax?.supplier?.amount) }}
                          {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="order-modal-body-content-block">
                  <div class="order-modal-body-content-block-header p-[0.75rem]">Total cost</div>
                  <div class="order-modal-body-content-block-body flex flex-col">
                    <div class="flex w-full">
                      <div class="order-modal-body-content-block-body-header w-6/12 pl-3">
                        <div
                          class="el-border order-modal-body-content-block-body-header-el my-[0.5rem]"
                        >
                          With Official Taxes
                        </div>
                      </div>
                      <div class="order-modal-body-content-block-body-header w-6/12 pl-3">
                        <div class="order-modal-body-content-block-body-header-el my-[0.5rem]">
                          With Supplier-Defined Taxes
                        </div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div class="el-border w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="order-modal-body-content-block-body-name w-8/12">Fuel</div>
                        <div class="order-modal-body-content-block-body-value w-4/12">
                          {{ formatNumber(supplyFuelDetails?.fuel_price?.amount) }}
                          {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                      <div class="w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="order-modal-body-content-block-body-name w-8/12">Fuel</div>
                        <div class="order-modal-body-content-block-body-value w-4/12">
                          {{ formatNumber(supplyFuelDetails?.fuel_price?.amount) }}
                          {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div class="el-border w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="order-modal-body-content-block-body-name w-8/12">Fees</div>
                        <div class="order-modal-body-content-block-body-value w-4/12">
                          {{ formatNumber(supplyFuelDetails?.fees?.total) }}
                          {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                      <div class="w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="order-modal-body-content-block-body-name w-8/12">Fees</div>
                        <div class="order-modal-body-content-block-body-value w-4/12">
                          {{ formatNumber(supplyFuelDetails?.fees?.client_total) }}
                          {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div class="el-border w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="order-modal-body-content-block-body-name w-8/12">Taxes</div>
                        <div class="order-modal-body-content-block-body-value w-4/12">
                          {{ formatNumber(supplyFuelDetails?.taxes?.official_total) }}
                          {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                      <div class="w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="order-modal-body-content-block-body-name w-8/12">Taxes</div>
                        <div class="order-modal-body-content-block-body-value w-4/12">
                          {{ formatNumber(supplyFuelDetails?.taxes?.supplier_total) }}
                          {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div
                        class="el-border results w-6/12 flex px-[0.75rem] py-[1rem] items-center"
                      >
                        <div class="order-modal-body-content-block-body-name w-8/12">
                          Total Uplift Cost
                        </div>
                        <div class="order-modal-body-content-block-body-value w-4/12">
                          {{ formatNumber(supplyFuelDetails?.total_official_taxes) }}
                          {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                      <div class="w-6/12 results flex px-[0.75rem] py-[1rem] items-center">
                        <div class="order-modal-body-content-block-body-name w-8/12">
                          Total Uplift Cost
                        </div>
                        <div class="order-modal-body-content-block-body-value w-4/12">
                          {{ formatNumber(supplyFuelDetails?.total) }}
                          {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="order-modal-body-content-block">
                  <div class="order-modal-body-content-block-header p-[0.75rem]">
                    Exchange Rates
                  </div>
                  <div
                    v-if="Object.keys(supplyFuel?.scenario?.used_currency_rates).length > 0"
                    class="order-modal-body-content-block-body flex px-[0.75rem] py-[1rem]"
                  >
                    <div class="order-modal-body-content-block-body-name w-8/12 flex flex-col">
                      Open Exchange Rates
                      <div class="order-modal-body-content-block-body-sub">
                        Valid at
                        {{
                          toRateTime(
                            supplyFuel?.scenario?.used_currency_rates?.[
                              Object.keys(supplyFuel?.scenario?.used_currency_rates)[0]
                            ]?.timestamp + '000'
                          )
                        }}
                      </div>
                    </div>
                    <div
                      class="order-modal-body-content-block-body-value w-4/12 flex items-center justify-end"
                    >
                      {{
                        supplyFuel?.scenario?.used_currency_rates?.[
                          Object.keys(supplyFuel?.scenario?.used_currency_rates)[0]
                        ]?.rate
                      }}
                      {{ JSON.parse(Object.keys(supplyFuel?.scenario?.used_currency_rates)[0])[0] }}
                      ->
                      {{ JSON.parse(Object.keys(supplyFuel?.scenario?.used_currency_rates)[0])[1] }}
                    </div>
                  </div>
                  <div
                    v-else
                    class="results order-modal-body-content-block-body flex flex-col items-center justify-center px-[0.75rem] py-6"
                  >
                    <div
                      class="order-modal-body-content-block-body-name flex flex-col items-center"
                    >
                      No exchange rates found
                    </div>
                  </div>
                </div>
                <div class="order-modal-body-content-block">
                  <div class="order-modal-body-content-block-header p-[0.75rem]">
                    Fuel-related NOTAMs
                  </div>
                  <div
                    v-if="
                      supplyFuelDetails?.notams?.length && supplyFuelDetails?.notams?.length > 0
                    "
                    class="order-modal-body-content-block-body flex flex-col px-[0.75rem] py-[0.75rem]"
                  >
                    <div
                      v-for="(notam, notamId) in supplyFuelDetails?.notams"
                      :key="notamId"
                      class="order-modal-body-content-block-body-name flex flex-col"
                    >
                      <div>
                        {{ notam.effective_start }} - {{ notam.effective_end ?? 'PERM' }} Status:
                        {{ notam.status }}
                      </div>
                      <div v-text="notam.text"></div>
                    </div>
                    <div class="order-modal-body-content-block-body-sub">
                      The FAA NOTAMs API was last chacked for this location at
                      {{ supplyFuelDetails?.notams_last_check }}
                    </div>
                  </div>
                  <div
                    v-else
                    class="results order-modal-body-content-block-body flex flex-col items-center justify-center px-[0.75rem] py-6"
                  >
                    <div
                      class="order-modal-body-content-block-body-name flex flex-col items-center"
                    >
                      No fuel-related NOTAMs found
                    </div>
                    <div class="order-modal-body-content-block-body-sub">
                      The FAA NOTAMs API was last chacked for this location at
                      {{ supplyFuelDetails?.notams_last_check }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </ScrollBar>
        <div class="order-modal-footer flex justify-end">
          <div class="order-modal-footer-el flex justify-between w-6/12">
            <div v-if="!isLoadingSupplierFuelDetails" class="order-modal-footer-el-name">
              Total Uplift Cost
            </div>
            <div v-if="!isLoadingSupplierFuelDetails" class="order-modal-footer-el-value">
              {{ formatNumber(supplyFuelDetails?.total) }} {{ supplyFuelDetails?.currency?.code }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, type PropType, ref } from 'vue';
import { onClickOutside } from '@vueuse/core';
import { useQuerySupplierFuelDetails } from '@/services/queries';
import { addThousandSeparators, formatNumber, toRateTime } from '@/helpers/order';
import Loading from '../forms/Loading.vue';
import ScrollBar from '../forms/ScrollBar.vue';

import type { ISupplierFuel } from 'shared/types';

const props = defineProps({
  isOpen: Boolean,
  isOpenRelease: Boolean,
  supplyFuel: {
    type: Object as PropType<ISupplierFuel>,
    default: null
  },
  resultIndex: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['modal-close', 'modal-submit']);

const target = ref(null);

onClickOutside(target, () => emit('modal-close'));

const selectedSupplierInfo = computed(() =>
  props.supplyFuel != null && props.resultIndex != null
    ? {
        supplierId: props.supplyFuel?.id,
        detailsId: Number(props.supplyFuel?.results[props.resultIndex].key)
      }
    : null
);

const { data: supplyFuelDetails, isPending: isLoadingSupplierFuelDetails } =
  useQuerySupplierFuelDetails(selectedSupplierInfo);
</script>

<style scoped lang="scss">
.supply-fuel-modal {
  .order-modal-container {
    width: 700px;
  }

  .form-body-wrapper {
    max-height: 820px;
    overflow-y: auto;
  }

  .order-modal-header {
    color: rgba(39, 44, 63, 1);
    font-size: 18px;
    font-weight: 600;
    padding: 1.25rem 1.5rem 1.25rem 1.5rem;
  }

  .order-modal-body {
    max-height: 70vh;

    &-header {
      border-top: 1px solid rgba(223, 226, 236, 1);
      border-bottom: 1px solid rgba(223, 226, 236, 1);
      padding: 1rem 1.5rem 1rem 1.5rem;

      &-el {
        align-items: baseline;

        &-name {
          font-size: 13px;
          color: rgba(82, 90, 122, 1);
          font-weight: 500;
        }

        &-data {
          font-size: 14px;
          color: theme('colors.main');
          font-weight: 500;
        }
      }

      &-content {
        padding: 0.75rem;
      }
    }

    .issues {
      background-color: rgba(255, 161, 0, 0.08);
    }

    .results {
      background-color: rgb(246, 248, 252);
    }

    .el-border {
      border-right: 1px solid rgb(223, 226, 236);
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
      bottom: 1.5rem;
      left: 0;
      min-width: 27vw;

      li {
        font-size: 12px;
        font-weight: 400;
      }

      &::before {
        content: '';
        position: absolute;
        width: 10px;
        height: 10px;
        background-color: rgb(81, 93, 138);
        transform: rotate(45deg);
        left: 6.7rem;
        bottom: -5px;
      }

      &.left-tooltip {
        right: 0;
        left: unset;

        &::before {
          right: 50%;
          left: unset;
          bottom: -5px;
        }
      }
    }

    &-content {
      background-color: theme('colors.dark-background');

      &-wrap {
        background-color: theme('colors.dark-background');
      }

      &-block {
        border: 1px solid rgba(223, 226, 236, 1);
        border-radius: 6px;
        background-color: rgb(255, 255, 255);

        &-header {
          color: theme('colors.main');
          font-size: 15px;
          font-weight: 600;
          border-bottom: 1px solid rgba(223, 226, 236, 1);
        }

        &-body {
          color: rgba(39, 44, 63, 1);
          font-size: 14px;
          font-weight: 500;

          &-header {
            background-color: rgba(246, 248, 252, 1);
            color: rgba(82, 90, 122, 1);
            font-size: 11px;
            font-weight: 500;
          }

          &-name {
            color: rgba(39, 44, 63, 1);
            font-size: 13px;
            font-weight: 500;
            position: relative;
          }

          &-sub {
            color: rgba(82, 90, 122, 1);
            font-size: 12px;
            font-weight: 400;
          }

          &-desc {
            color: rgba(39, 44, 63, 1);
            font-size: 13px;
            font-weight: 400;
          }

          &-value {
            color: rgba(39, 44, 63, 1);
            font-size: 13px;
            font-weight: 600;
            text-align: end;
          }

          .issue-html {
            position: relative;

            &::before {
              content: '';
              position: absolute;
              height: 19px;
              width: 4px;
              background-color: rgba(254, 161, 22, 1);
              border-radius: 2px;
              left: -0.8rem;
            }
          }
        }
      }
    }

    .hover-wrap {
      &:hover {
        .order-modal-body-tooltip {
          display: block;
        }
      }
    }
  }

  .order-modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    border-top-width: 1px;
    border-color: rgb(75 85 99 / 0.25);
    background-color: rgba(246, 248, 252, 1);
    border-radius: 0 0 0.5rem 0.5rem;
    padding: 1.25rem 1.5rem 1.25rem 1.5rem;

    &-el {
      &-name {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 500;
      }

      &-value {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 600;
      }
    }

    .modal-button {
      display: flex;
      flex-shrink: 0;
      background-color: rgb(81 93 138) !important;
      padding: 0.5rem !important;
      padding-left: 1rem !important;
      padding-right: 1rem !important;
      color: rgb(255 255 255) !important;
      border-radius: 0.5rem !important;

      &.cancel {
        background-color: rgba(240, 242, 252, 1) !important;
        color: rgb(81 93 138) !important;
      }
    }
  }
}
</style>
