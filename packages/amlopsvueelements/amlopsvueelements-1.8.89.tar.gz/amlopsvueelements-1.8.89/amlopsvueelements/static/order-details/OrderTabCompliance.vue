<template>
  <div class="w-full h-auto flex flex-col gap-2">
    <div class="compliance-step bg-white w-full border border-transparent rounded-md">
      <div class="compliance-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="compliance-step-header-name">Management Approval</div>
        <div class="flex items-center gap-[1rem]">
          <Loading v-if="isFetchingRequestManagementApproval" />
          <Button
            v-if="isRequestManagementApprovalShown"
            class="button flex items-center gap-2"
            @disabled="isFetchingRequestManagementApproval ? 'true' : 'false'"
            @click="onRequestManagementApproval"
          >
            Request Management Approval
          </Button>
        </div>
      </div>
      <div
        class="compliance-step-content compliance-status w-full flex p-[0.75rem] gap-2"
        :class="{ 'items-center': isFetchingProceedCompliance }"
      >
        <Loading v-if="isFetchingProceedCompliance" />
        <div
          v-if="proceedComplianceData && !isFetchingProceedCompliance"
          class="compliance-step-content-el-name flex items-center"
        >
          Status
        </div>
        <div
          v-if="proceedComplianceData && !isFetchingProceedCompliance"
          class="compliance-step-content-el-value py-[0.25rem] px-[0.75rem]"
          :style="{
            backgroundColor: proceedComplianceData?.compliance_status?.background_color,
            color: proceedComplianceData?.compliance_status?.text_color
          }"
        >
          {{ proceedComplianceData.compliance_status.status }}
        </div>
      </div>
    </div>
    <div class="compliance-step bg-white w-full border border-transparent rounded-md">
      <div class="compliance-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="compliance-step-header-name">Compliance Checks</div>
      </div>
      <div class="compliance-step-content w-full flex flex-col">
        <div class="compliance-step-content-header-wrap w-full flex items-center">
          <div class="compliance-step-content-col pl-[0.75rem] py-[0.5rem] w-6/12">
            <div class="compliance-step-content-col-header uppercase el-border">Sanctions</div>
          </div>
          <div class="compliance-step-content-col w-6/12">
            <div class="compliance-step-content-col-header px-[0.75rem] py-[0.5rem] uppercase">
              Supplier Restrictions
            </div>
          </div>
        </div>
        <div class="compliance-step-content-data-wrap w-full flex items-start">
          <div class="compliance-step-content-col flex flex-col w-6/12">
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Client</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div
                  class="compliance-step-circle circle-green"
                  :class="{
                    'circle-yellow':
                      order?.compliance_checks?.sanctions?.is_client_sanctions_needs_review,
                    'circle-red': order?.compliance_checks?.sanctions?.is_client_sanctions_confirmed
                  }"
                >
                  <div class="icon"></div>
                </div>
                {{
                  order?.compliance_checks?.sanctions?.is_client_sanctions_needs_review
                    ? 'Needs Reviewing'
                    : order?.compliance_checks?.sanctions?.is_client_sanctions_confirmed
                    ? 'Sanctioned'
                    : 'OK'
                }}
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Operator</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div
                  class="compliance-step-circle circle-green"
                  :class="{
                    'circle-yellow':
                      order?.compliance_checks?.sanctions?.is_operator_sanctions_needs_review,
                    'circle-red':
                      order?.compliance_checks?.sanctions?.is_operator_sanctions_confirmed
                  }"
                >
                  <div class="icon"></div>
                </div>
                {{
                  order?.compliance_checks?.sanctions?.is_operator_sanctions_needs_review
                    ? 'Needs Reviewing'
                    : order?.compliance_checks?.sanctions?.is_operator_sanctions_confirmed
                    ? 'Sanctioned'
                    : 'OK'
                }}
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Aircraft</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div
                  class="compliance-step-circle circle-green"
                  :class="{
                    'circle-yellow':
                      order?.compliance_checks?.sanctions?.is_aircraft_sanctions_needs_review,
                    'circle-red':
                      order?.compliance_checks?.sanctions?.is_aircraft_sanctions_confirmed
                  }"
                >
                  <div class="icon"></div>
                </div>
                {{
                  order?.compliance_checks?.sanctions?.is_aircraft_sanctions_needs_review
                    ? 'Needs Reviewing'
                    : order?.compliance_checks?.sanctions?.is_aircraft_sanctions_confirmed
                    ? 'Sanctioned'
                    : 'OK'
                }}
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Uplift Country</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div
                  class="compliance-step-circle circle-green"
                  :class="{
                    'circle-red':
                      order?.compliance_checks?.sanctions?.is_uplift_country_sanctions_confirmed
                  }"
                >
                  <div class="icon"></div>
                </div>
                {{
                  order?.compliance_checks?.sanctions?.is_uplift_country_sanctions_confirmed
                    ? 'Sanctioned'
                    : 'OK'
                }}
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Destination Country</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div
                  class="compliance-step-circle circle-green"
                  :class="{
                    'circle-red':
                      order?.compliance_checks?.sanctions
                        ?.is_destination_country_sanctions_confirmed
                  }"
                >
                  <div class="icon"></div>
                </div>
                {{
                  order?.compliance_checks?.sanctions?.is_destination_country_sanctions_confirmed
                    ? 'Sanctioned'
                    : 'OK'
                }}
              </div>
            </div>
          </div>
          <div class="compliance-step-content-col flex flex-col w-6/12 el-border-left">
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Aircraft</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div
                  class="compliance-step-circle circle-green"
                  :class="{
                    'circle-red':
                      order?.compliance_checks?.supplier_restrictions?.aircraft_sanction_type_id ===
                      1,
                    'circle-yellow':
                      order?.compliance_checks?.supplier_restrictions?.aircraft_sanction_type_id ===
                      2
                  }"
                >
                  <div class="icon"></div>
                </div>
                {{
                  order?.compliance_checks?.supplier_restrictions?.aircraft_sanction_type_id === 1
                    ? 'Sanctioned'
                    : order?.compliance_checks?.supplier_restrictions?.aircraft_sanction_type_id ===
                      2
                    ? 'Embargoed'
                    : 'OK'
                }}
                <a
                  v-if="
                    order?.compliance_checks?.supplier_restrictions?.aircraft_sanctions_document_id
                  "
                  :href="order.compliance_checks.supplier_restrictions?.aircraft_sanctions_document_url!"
                  ><img src="../../assets/icons/chevron-down.svg" alt="document"
                /></a>
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">
                Aircraft Registration Prefix
              </div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div
                  class="compliance-step-circle circle-green"
                  :class="{
                    'circle-red':
                      order?.compliance_checks?.supplier_restrictions
                        ?.registration_sanction_type_id === 1,
                    'circle-yellow':
                      order?.compliance_checks?.supplier_restrictions
                        ?.registration_sanction_type_id === 2
                  }"
                >
                  <div class="icon"></div>
                </div>
                {{
                  order?.compliance_checks?.supplier_restrictions?.registration_sanction_type_id ===
                  1
                    ? 'Sanctioned'
                    : order?.compliance_checks?.supplier_restrictions
                        ?.registration_sanction_type_id === 2
                    ? 'Embargoed'
                    : 'OK'
                }}<a
                  v-if="
                    order?.compliance_checks?.supplier_restrictions
                      ?.registration_sanction_document_id
                  "
                  :href="order.compliance_checks.supplier_restrictions?.registration_sanction_document_url!"
                  ><img src="../../assets/icons/chevron-down.svg" alt="document"
                /></a>
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Uplift Airport</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div
                  class="compliance-step-circle circle-green"
                  :class="{
                    'circle-red':
                      order?.compliance_checks?.supplier_restrictions
                        ?.uplift_airport_sanction_type_id === 1,
                    'circle-yellow':
                      order?.compliance_checks?.supplier_restrictions
                        ?.uplift_airport_sanction_type_id === 2
                  }"
                >
                  <div class="icon"></div>
                </div>
                {{
                  order?.compliance_checks?.supplier_restrictions
                    ?.uplift_airport_sanction_type_id === 1
                    ? 'Sanctioned'
                    : order?.compliance_checks?.supplier_restrictions
                        ?.uplift_airport_sanction_type_id === 2
                    ? 'Embargoed'
                    : 'OK'
                }}<a
                  v-if="
                    order?.compliance_checks?.supplier_restrictions
                      ?.uplift_airport_sanction_document_id
                  "
                  :href="order.compliance_checks.supplier_restrictions?.uplift_airport_sanction_document_url!"
                  ><img src="../../assets/icons/chevron-down.svg" alt="document"
                /></a>
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Destination Airport</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div
                  class="compliance-step-circle circle-green"
                  :class="{
                    'circle-red':
                      order?.compliance_checks?.supplier_restrictions
                        ?.destination_airport_sanction_type_id === 1,
                    'circle-yellow':
                      order?.compliance_checks?.supplier_restrictions
                        ?.destination_airport_sanction_type_id === 2
                  }"
                >
                  <div class="icon"></div>
                </div>
                {{
                  order?.compliance_checks?.supplier_restrictions
                    ?.destination_airport_sanction_type_id === 1
                    ? 'Sanctioned'
                    : order?.compliance_checks?.supplier_restrictions
                        ?.destination_airport_sanction_type_id === 2
                    ? 'Embargoed'
                    : 'OK'
                }}<a
                  v-if="
                    order?.compliance_checks?.supplier_restrictions
                      ?.destination_airport_sanction_document_id
                  "
                  :href="order.compliance_checks.supplier_restrictions?.destination_airport_sanction_document_url!"
                  ><img src="../../assets/icons/chevron-down.svg" alt="document"
                /></a>
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Uplift Country</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div
                  class="compliance-step-circle circle-green"
                  :class="{
                    'circle-red':
                      order?.compliance_checks?.supplier_restrictions
                        ?.uplift_country_sanction_type_id === 1,
                    'circle-yellow':
                      order?.compliance_checks?.supplier_restrictions
                        ?.uplift_country_sanction_type_id === 2
                  }"
                >
                  <div class="icon"></div>
                </div>
                {{
                  order?.compliance_checks?.supplier_restrictions
                    ?.uplift_country_sanction_type_id === 1
                    ? 'Sanctioned'
                    : order?.compliance_checks?.supplier_restrictions
                        ?.uplift_country_sanction_type_id === 2
                    ? 'Embargoed'
                    : 'OK'
                }}<a
                  v-if="
                    order?.compliance_checks?.supplier_restrictions
                      ?.uplift_country_sanction_document_id
                  "
                  :href="order.compliance_checks.supplier_restrictions?.uplift_country_sanction_document_url!"
                  ><img src="../../assets/icons/chevron-down.svg" alt="document"
                /></a>
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Destination Country</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div
                  class="compliance-step-circle circle-green"
                  :class="{
                    'circle-red':
                      order?.compliance_checks?.supplier_restrictions
                        ?.destination_country_sanction_type_id === 1,
                    'circle-yellow':
                      order?.compliance_checks?.supplier_restrictions
                        ?.destination_country_sanction_type_id === 2
                  }"
                >
                  <div class="icon"></div>
                </div>
                {{
                  order?.compliance_checks?.supplier_restrictions
                    ?.destination_country_sanction_type_id === 1
                    ? 'Sanctioned'
                    : order?.compliance_checks?.supplier_restrictions
                        ?.destination_country_sanction_type_id === 2
                    ? 'Embargoed'
                    : 'OK'
                }}<a
                  v-if="
                    order?.compliance_checks?.supplier_restrictions
                      ?.destination_country_sanction_document_id
                  "
                  :href="order.compliance_checks.supplier_restrictions?.destination_country_sanction_document_url!"
                  ><img src="../../assets/icons/chevron-down.svg" alt="document"
                /></a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <AircraftRecentDestinations :order="props.order" />
      <OrderTabComplianceNotams :selected-supplier-info="props.selectedSupplierInfo" />
    </div>
    <div class="compliance-step bg-white w-full border border-transparent rounded-md">
      <div class="compliance-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="compliance-step-header-name">Client Credit Exposure</div>
      </div>
      <div class="compliance-step-content compliance-credit w-full flex flex-col gap-2">
        <CreditExposure />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, type PropType, shallowRef, watch } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { Button } from 'shared/components';
import { useOrderStore } from '@/stores/useOrderStore';
import { useQueryProceedCompliance, useQueryRequestManagementApproval } from '@/services/queries';
import { notify } from '@/helpers/toast';
import { AircraftRecentDestinations, OrderTabComplianceNotams } from '../datacomponent';
import CreditExposure from '../datacomponent/CreditExposure.vue';
import Loading from '../forms/Loading.vue';

import type { IOrder, SelectedSupplierInfo } from 'shared/types';

const props = defineProps({
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  order: {
    type: Object as PropType<IOrder>,
    default: null
  },
  selectedSupplierInfo: {
    type: Object as PropType<SelectedSupplierInfo | null>,
    default: null
  }
});

const queryClient = useQueryClient();
const orderStore = useOrderStore();

const wasOrderApprovalMessageShown = shallowRef(false);

const orderId = computed(() => orderStore.orderId);
const isCurrentStep = computed(
  () => orderStore.currentStep === 2 && orderStore.order?.type?.is_fuel
);

const {
  data: proceedComplianceData,
  isFetching: isFetchingProceedCompliance,
  status: proceedComplianceStatus
} = useQueryProceedCompliance(orderId, {
  enabled: isCurrentStep,
  retry: false
});

const {
  refetch: refetchRequestManagementApproval,
  isFetching: isFetchingRequestManagementApproval
} = useQueryRequestManagementApproval(orderId, {
  enabled: false
});

const isRequestManagementApprovalShown = computed(
  () =>
    proceedComplianceData.value &&
    proceedComplianceData.value.order_approval?.is_auto_approved === false &&
    proceedComplianceData.value.order_approval?.is_approved === null &&
    proceedComplianceData.value.order_approval?.requested_at === null
);

const onRequestManagementApproval = async () => {
  await refetchRequestManagementApproval();
  queryClient.invalidateQueries({ queryKey: ['proceedCompliance', orderId] });
  queryClient.invalidateQueries({ queryKey: ['orderStatus', orderId] });
};

watch(proceedComplianceData, (data) => {
  if (proceedComplianceStatus.value === 'success' && data) {
    const shouldNotify =
      data.order_approval?.messages?.length && !wasOrderApprovalMessageShown.value;

    if (shouldNotify) {
      notify(data.order_approval?.messages?.join('\n'), 'error');
      wasOrderApprovalMessageShown.value = true;
    }
  }
});
</script>

<style lang="scss">
.compliance-step {
  .button {
    background-color: rgba(81, 93, 138, 1) !important;
    color: white !important;
    font-weight: 500 !important;
    font-size: 15px !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-2 px-4 rounded-xl #{!important};
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

  &-circle {
    width: 20px;
    height: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;

    .icon {
      height: 12px;
      width: 12px;
      z-index: 1;
    }

    &.circle-green {
      background-color: rgba(11, 161, 125, 0.12);

      .icon {
        background-image: url('../../assets/icons/status-check.svg');
      }
    }

    &.circle-yellow {
      background-color: rgba(254, 161, 22, 0.12);

      .icon {
        background-image: url('../../assets/icons/status-alert.svg');
      }
    }

    &.circle-red {
      background-color: rgba(254, 98, 98, 1);

      .icon {
        background-image: url('../../assets/icons/status-close.svg');
      }
    }

    &.circle-gray {
      background-color: rgba(139, 148, 178, 0.12);

      .icon {
        background-image: url('../../assets/icons/status-help.svg');
      }
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

    &-el {
      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 13px;
        font-weight: 500;
        min-width: 180px;
      }

      &-value {
        border-radius: 6px;
        border: 1px solid transparent;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
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

    &-col {
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
          align-items: center;

          img {
            transform: rotate(270deg);
            filter: brightness(0) saturate(100%) invert(71%) sepia(11%) saturate(607%)
              hue-rotate(189deg) brightness(93%) contrast(89%);
            width: 12px;
            height: 12px;
          }
        }
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
        .compliance-step-info-side {
          padding-top: 18px;
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

      .compliance-step-info {
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
            min-width: 8px;
            min-height: 8px;
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
            height: 18px;
            top: 6px;
            left: 1.5px;
          }
        }
      }

      .compliance-step-data {
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
}
</style>
