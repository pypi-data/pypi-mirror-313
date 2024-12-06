<template>
  <div class="w-full h-auto flex flex-col gap-2">
    <SendQuoteModal
      ref="quoteModal"
      :handlers="quoteHandlers!"
      :is-open="modalOpened === 'quote'"
      name="order-modal"
      @modal-close="closeModal"
    />
    <AddServiceCommentModal
      v-if="modalOpened === 'comment'"
      ref="commentModal"
      :is-open="modalOpened === 'comment'"
      name="order-modal"
      :header="
        activeService?.handling_service?.full_repr ??
        activeService?.handling_service?.name ??
        'Add Comment'
      "
      :model-value="activeService?.comment ?? ''"
      @modal-submit="onUpdateService('comment', $event, activeServiceIndex!)"
      @modal-close="closeModal"
    />
    <ConfirmationModal
      :is-open="modalOpened === 'delete'"
      title="Are you sure you want to delete this service?"
      subtitle="This action cannot be undone."
      cancel-button="No"
      confirm-button="Yes"
      @modal-confirm="onDeleteService(activeServiceIndex!)"
      @modal-close="closeModal"
    />
    <EnterQuoteDetailsModal
      :is-open="modalOpened === 'quote-details'"
      :quote="activeQuote"
      @modal-close="closeModal"
    />
    <div class="handling-step bg-white w-full border border-transparent rounded-md">
      <div class="handling-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="handling-step-header-name">Ground Handling Services</div>
        <div class="loading-wrap">
          <Loading v-if="isUpdating" />
        </div>
      </div>
      <div v-if="!isLoadingServices" class="handling-step-content">
        <div class="handling-step-content-header-sub flex">
          <div
            class="handling-step-content-header-sub-wrap flex w-8/12 py-[0.5rem] pl-[0.75rem] gap-2"
          >
            <div class="handling-step-content-header-sub-el flex w-6/12 justify-start">Item</div>
            <div
              class="handling-step-content-header-sub-el flex w-6/12 justify-start el-border pl-4"
            >
              Quantity
            </div>
          </div>
          <div class="handling-step-content-header-sub-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]">
            <div class="handling-step-content-header-sub-el flex w-6/12 justify-center">
              Arrival
            </div>
            <div class="handling-step-content-header-sub-el flex w-6/12 justify-center">
              Departure
            </div>
            <div class="handling-step-content-header-sub-el flex w-full justify-start">&nbsp;</div>
          </div>
        </div>
        <div
          v-for="(service, index) in orderServices"
          :key="index"
          class="handling-step-content-element flex"
        >
          <div
            class="handling-step-content-element-wrap flex w-8/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="handling-step-content-element-el-name flex justify-start items-center w-6/12"
            >
              {{ service.handling_service.full_repr }}
            </div>
            <div
              class="handling-step-content-element-el flex justify-start items-center w-6/12 pr-[0.75rem]"
            >
              <span class="text-light-subtitle pr-[0.5rem] text-[0.75rem]">x</span>
              <div v-if="!service.is_editable" class="flex gap-2">
                {{ service.quantity_text ?? '--' }}
                {{ service.quantity_value ?? '' }}
                {{ service.quantity_uom ?? '' }}
              </div>
              <InputField
                v-else-if="service.handling_service.is_allowed_free_text"
                :model-value="(service.quantity_text) as string"
                class="w-full mb-0"
                is-white
                placeholder=" "
                @update:model-value="debounceUpdateService('quantity_text', $event, index)"
              />
              <div
                v-else-if="service.handling_service.is_allowed_quantity_selection"
                class="input-wrap flex w-full items-center"
              >
                <InputField
                  :model-value="(service.quantity_value) as string"
                  class="w-6/12 mb-0"
                  is-white
                  is-half
                  placeholder=" "
                  @update:model-value="debounceUpdateService('quantity_value', $event, index)"
                />
                <SelectField
                  class="w-6/12 mb-0"
                  :is-white="true"
                  :is-half="true"
                  placeholder=" "
                  disabled
                  label="description_plural"
                  :model-value="service.quantity_uom!"
                  @update:model-value="onUpdateService('quantity_uom', $event, index)"
                />
              </div>
              <div v-else class="flex gap-2">--</div>
            </div>
          </div>
          <div
            class="handling-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="handling-step-content-element-el-name flex justify-center items-center w-6/12"
            >
              <CheckboxField
                :model-value="service.applies_on_arrival"
                class="mb-0 mr-1"
                :size="'20px'"
                :disabled="!service.is_editable || !service.handling_service.is_arr_available"
                @update:model-value="onUpdateService('applies_on_arrival', $event, index)"
              ></CheckboxField>
            </div>
            <div class="handling-step-content-element-el flex justify-center items-center w-6/12">
              <CheckboxField
                :model-value="service.applies_on_departure"
                class="mb-0 mr-1"
                :size="'20px'"
                :disabled="!service.is_editable || !service.handling_service.is_dep_available"
                @update:model-value="onUpdateService('applies_on_departure', $event, index)"
              ></CheckboxField>
            </div>
            <div
              class="handling-step-content-element-el flex justify-between items-center w-full px-[0.5rem]"
            >
              <div v-if="service.comment" class="relative">
                <div class="hover-wrap contents">
                  <img
                    width="44"
                    height="44"
                    src="../../assets/icons/message-text-square.svg"
                    alt="comment"
                    class="comment-button cursor-pointer p-[0.75rem] rounded-lg"
                    @click="openModal('comment', index)"
                  />
                  <div class="handling-step-tooltip">
                    <div>{{ service.comment }}</div>
                  </div>
                </div>
              </div>
              <img
                v-else
                width="44"
                height="44"
                src="../../assets/icons/message-plus-square.svg"
                alt="comment"
                class="cursor-pointer p-[0.75rem] rounded-lg"
                @click="openModal('comment', index)"
              />

              <img
                v-if="service.is_deletable"
                width="20"
                height="20"
                src="../../assets/icons/cross-red.svg"
                alt="delete"
                class="cursor-pointer"
                @click="openModal('delete', index)"
              />
            </div>
          </div>
        </div>
        <AddServiceToOrder v-if="orderId" :order="order" :current-tab="1" />
      </div>
      <div v-else class="handling-step-content py-[3rem]">
        <Loading />
      </div>
    </div>
    <div class="handling-step bg-white w-full border border-transparent rounded-md">
      <div class="handling-step-header flex justify-between items-center py-[0.5rem] px-[0.75rem]">
        <div class="handling-step-header-name">Ground Handling Quotes</div>
        <Button class="button flex items-center gap-2" @click="openQuoteModal">
          Send Quote Request
        </Button>
      </div>
      <div
        v-if="ghQuotes?.length === 0"
        class="handling-step-content-missing flex items-center justify-center py-[1.25rem]"
      >
        <Loading v-if="isGhQuotesPending" />
        <span>There are no quotes yet</span>
      </div>
      <div v-else class="handling-step-content w-full flex flex-col">
        <div class="handling-step-content-header-wrap w-full flex items-center">
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">
              Station Name
            </div>
          </div>
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">Brand</div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">Status</div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem] text-right">
              Total Cost
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">&nbsp;</div>
          </div>
        </div>
        <div
          v-for="(quote, index) in ghQuotes"
          :key="index"
          class="handling-step-content-data-wrap w-full flex items-center"
        >
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem]">
              <div
                class="flex gap-1 align-center cursor-pointer w-fit"
                @click="redirectToURL(quote.supplier?.url)"
              >
                {{ quote.supplier?.full_repr }}
                <img
                  v-if="quote.supplier?.url"
                  width="12"
                  height="12"
                  src="../../assets/icons/chevron-right.svg"
                  alt="warn"
                  class="warn"
                />
              </div>
            </div>
          </div>
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem]">
              <div
                class="flex gap-1 align-center cursor-pointer w-fit"
                @click="redirectToURL(quote.supplier?.handling_brand?.url)"
              >
                {{ quote.supplier?.handling_brand?.full_repr }}
                <img
                  v-if="quote.supplier?.handling_brand?.url"
                  width="12"
                  height="12"
                  src="../../assets/icons/chevron-right.svg"
                  alt="warn"
                  class="warn"
                />
              </div>
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="flex">
              <div
                class="handling-step-content-col-data px-[0.75rem] py-[0.25rem] rounded-md uppercase max-w-fit"
                :style="{
                  'background-color': quote?.status?.background_color,
                  color: quote?.status?.color
                }"
              >
                {{ quote?.status?.name }}
              </div>
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem] text-right">
              {{ formatNumber(quote?.quote_total_value!) ?? '--' }}
              {{ quote?.quote_currency?.code ?? '' }}
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div
              class="handling-step-content-col-data px-[0.75rem] py-[0.5rem] flex justify-center"
            >
              <Button v-if="true" class="button light-button" @click="editQuote(quote)">
                <img width="20" height="20" :src="getImageUrl('assets/icons/edit.svg')" alt="edit"
              /></Button>
              <div v-else class="flex items-center justify-center p-[0.5rem]" @click="() => {}">
                <img
                  width="20"
                  height="20"
                  :src="getImageUrl('assets/icons/eye.svg')"
                  alt="details"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-if="isGhQuotesPending"
        class="handling-step-content w-full flex py-8 px-[0.75rem] flex flex-col"
      >
        <Loading />
      </div>
    </div>
    <div class="handling-step bg-white w-full border border-transparent rounded-md">
      <div class="handling-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="handling-step-header-name">Ground Handler Selection</div>
        <div class="loading-wrap">
          <Loading v-if="isSelectOrderHandlerPending" />
        </div>
      </div>
      <div class="handling-step-content w-full flex flex-col">
        <div class="handling-step-content-header-wrap w-full flex items-center">
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">
              Station Name
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">Brand</div>
          </div>
          <div class="handling-step-content-col w-1/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">
              Handles Mil?
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">
              Pricing Details
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem] text-right">
              Estimated Total Cost
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">&nbsp;</div>
          </div>
        </div>
        <div
          v-for="(handler, index) in groundHandlers"
          :key="index"
          class="handling-step-content-data-wrap w-full flex items-center"
          :class="{
            'selected-supplier':
              order?.gh_order?.ground_handler?.id === handler?.id ||
              selectedHandler?.id === handler?.id,

            'handler-selection': !(
              selectedHandler === null && order?.gh_order?.ground_handler === null
            )
          }"
        >
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem]">
              <div
                class="flex gap-1 align-center cursor-pointer w-fit"
                @click="redirectToURL(handler?.url)"
              >
                {{ handler.full_repr }}
                <img
                  v-if="handler.url"
                  width="12"
                  height="12"
                  src="../../assets/icons/chevron-right.svg"
                  alt="warn"
                  class="warn"
                />
              </div>
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem]">
              <div class="flex gap-1 align-center w-fit">
                <div>
                  <span class="cursor-pointer">{{ handler.handling_brand?.full_repr }}</span>
                  <img
                    v-if="handler.handling_brand?.url"
                    width="12"
                    height="12"
                    src="../../assets/icons/chevron-right.svg"
                    alt="warn"
                    class="warn cursor-pointer ml-[0.25rem]"
                    @click="redirectToURL(handler.handling_brand?.url)"
                  />
                </div>
              </div>
            </div>
          </div>
          <div class="handling-step-content-col w-1/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ handler.handles_military ? 'Yes' : 'No' }}
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="flex">
              <div
                class="handling-step-content-col-data px-[0.75rem] py-[0.25rem] rounded-md uppercase text-center"
              >
                {{ handler.pricing_details?.pricing_source_name }}
              </div>
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem] text-right">
              {{
                handler.pricing_details?.pricing_total_value
                  ? formatNumber(handler.pricing_details?.pricing_total_value)
                  : '--'
              }}
              {{ handler.pricing_details?.pricing_currency?.code ?? '' }}
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div
              class="handling-step-content-col-data px-[0.75rem] py-[0.5rem] flex justify-center"
            >
              <Button
                v-if="selectedHandler === null && order?.gh_order?.ground_handler === null"
                class="button"
                @click="selectHandler(handler)"
                >Select</Button
              >
              <div v-else class="selection-tick flex items-center justify-center">
                <img width="20" height="20" src="../../assets/icons/check.svg" alt="check" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-if="groundHandlers?.length === 0"
        class="handling-step-content-none w-full flex py-[1rem] pr-[0.75rem] pl-[2.5rem] flex flex-col"
      >
        <img width="20" height="20" src="../../assets/icons/alert.svg" alt="warn" class="warn" />
        <div class="handling-step-content-none-header">
          There are no supplier ground handlers options available at this location
        </div>
      </div>
      <div
        v-if="isGroundHandlersPending"
        class="handling-step-content w-full flex py-8 px-[0.75rem] flex flex-col"
      >
        <Loading />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, type PropType, type Ref, ref, toRaw, watch } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { useDebounceFn } from '@vueuse/core';
import { Button } from 'shared/components';
import { useOrderStore } from '@/stores/useOrderStore';
import {
  useMutationAddOrderService,
  useMutationCreateOrderService,
  useMutationDeleteOrderService,
  useMutationSelectOrderHandler,
  useMutationUpdateOrderService
} from '@/services/mutations';
import {
  useQueryOrderGroundHandlers,
  useQueryOrderQuoteHandlers,
  useQueryOrderQuotes,
  useQueryOrderServices
} from '@/services/queries';
import { getImageUrl, redirectToURL } from '@/helpers';
import { formatNumber } from '@/helpers/order';
import AddServiceToOrder from '../datacomponent/AddServiceToOrder.vue';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import Loading from '../forms/Loading.vue';
import AddServiceCommentModal from '../modals/AddServiceCommentModal.vue';
import ConfirmationModal from '../modals/ConfirmationModal.vue';
import EnterQuoteDetailsModal from '../modals/EnterQuoteDetailsModal.vue';
import SendQuoteModal from '../modals/SendQuoteModal.vue';

import type { IOrder, IOrderQuote, IOrderQuoteHandler, IOrderService } from 'shared/types';

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
const orderId = computed(() => orderStore.order?.id);

const activeService: Ref<IOrderService | null | undefined> = ref(null);
const activeServiceIndex: Ref<number | null> = ref(null);
const activeQuote: Ref<IOrderQuote | null | undefined> = ref(null);
const modalOpened: Ref<'quote' | 'comment' | 'delete' | 'quote-details' | null> = ref(null);

const orderServices: Ref<IOrderService[]> = ref([]);
const enabled = ref(false);

const queryClient = useQueryClient();

const isUpdating = computed(
  () =>
    isAddOrderServicePending.value ||
    isCreateServicePending.value ||
    isUpdateOrderServicePending.value ||
    isDeleteServicePending.value
);

const openQuoteModal = () => {
  modalOpened.value = 'quote';
};
const openModal = (modalName: 'comment' | 'delete', index: number) => {
  activeService.value = orderServices.value?.[index];
  activeServiceIndex.value = index;

  modalOpened.value = modalName;
};
const closeModal = () => {
  modalOpened.value = null;
};

const editQuote = (quote: IOrderQuote) => {
  modalOpened.value = 'quote-details';
  activeQuote.value = quote;
};

const selectedHandler: Ref<IOrderQuoteHandler | null> = ref(null);
const selectHandler = async (handler: IOrderQuoteHandler) => {
  await onSelectedHandler(handler);
  selectedHandler.value = handler;
};

const { data: fetchedOrderServices, isLoading: isLoadingServices } = useQueryOrderServices(
  orderId,
  {
    enabled
  }
);
const { data: ghQuotes, isPending: isGhQuotesPending } = useQueryOrderQuotes(orderId, { enabled });
const { data: groundHandlers, isPending: isGroundHandlersPending } = useQueryOrderGroundHandlers(
  orderId,
  { enabled }
);
const { data: quoteHandlers } = useQueryOrderQuoteHandlers(orderId, { enabled });

const { mutate: updateOrderServiceMutation, isPending: isUpdateOrderServicePending } =
  useMutationUpdateOrderService();

const { isPending: isAddOrderServicePending } = useMutationAddOrderService();

const { isPending: isCreateServicePending } = useMutationCreateOrderService();

const { mutate: deleteServiceMutation, isPending: isDeleteServicePending } =
  useMutationDeleteOrderService();

const { mutate: selectOrderHandlerMutation, isPending: isSelectOrderHandlerPending } =
  useMutationSelectOrderHandler();

const debounceUpdateService = useDebounceFn(
  async (propName: string, value: any, serviceId: number) =>
    onUpdateService(propName, value, serviceId),
  1000
);

const onUpdateService = async (propName: string, value: any, serviceId: number) => {
  if (value !== '') {
    (orderServices.value![serviceId] as any)[propName] = value;
    const payload: any = {
      applies_on_arrival: orderServices.value![serviceId].applies_on_arrival,
      applies_on_departure: orderServices.value![serviceId].applies_on_departure,
      quantity_value: orderServices.value![serviceId].quantity_value,
      comment: orderServices.value![serviceId].comment
    };
    payload[propName] = value;
    await updateOrderServiceMutation(
      {
        orderId: props.order.id!,
        handlingServiceId: orderServices.value![serviceId].id!,
        payload
      },
      {
        onSuccess: () => {
          queryClient.invalidateQueries({ queryKey: ['orderServices', props.order.id] });
        }
      }
    );
  }
};

const onDeleteService = async (serviceId: number) => {
  closeModal();
  await deleteServiceMutation(
    {
      orderId: props.order.id!,
      handlingServiceId: orderServices.value![serviceId].id!
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['handlingServices', props.order.id] });
        queryClient.invalidateQueries({ queryKey: ['orderServices', props.order.id] });
      }
    }
  );
};

const onSelectedHandler = async (handler: any) => {
  if (handler) {
    await selectOrderHandlerMutation(
      {
        orderId: props.order.id!,
        payload: {
          ground_handler: handler.id
        }
      },
      {
        onSuccess: async () => {
          await orderStore.fetchOrder(props.order.id!);
        }
      }
    );
  }
};

watch(
  () => fetchedOrderServices.value,
  (data) => {
    orderServices.value = toRaw(data) ?? [];
  }
);

watch(
  () => props.order,
  async (order: IOrder) => {
    if (order && order.id && order.type.is_gh) {
      enabled.value = true;
    } else {
      enabled.value = false;
    }
  }
);
</script>

<style lang="scss">
.handling-step {
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

  .el-border {
    border-right: 1px solid rgb(223, 226, 236);

    &-light {
      border-right: 1px solid theme('colors.dark-background');
    }
  }

  .hover-wrap {
    &:hover {
      .handling-step-tooltip {
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
    top: -3rem;
    right: -13px;
    min-width: 10vw;

    &::before {
      content: '';
      position: absolute;
      width: 10px;
      height: 10px;
      background-color: rgb(81, 93, 138);
      transform: rotate(45deg);
      right: 1.9rem;
      bottom: -5px;
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

      &.handler-selection {
        background-color: rgba(246, 248, 252, 0.5);
        .handling-step-content-col-data {
          background-color: rgba(246, 248, 252, 0.5);
          color: rgb(133, 141, 173);
        }
      }

      &:last-of-type {
        border-radius: 0 0 8px 8px;
      }

      .selection-tick {
        display: none;
      }

      &.selected-supplier {
        background: #f1faf7 !important;

        .handling-step-content-col-data {
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

        .comment-button {
          background-color: rgba(240, 242, 252, 1);
        }

        &-name {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 500;
        }
      }

      &.new-service-element {
        background-color: #fbfcfe;
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
        color: rgba(39, 44, 63, 1);
        background-color: rgba(255, 255, 255, 1);
        font-size: 13px;
        font-weight: 400;

        .warn {
          filter: brightness(0) saturate(100%) invert(89%) sepia(7%) saturate(740%)
            hue-rotate(193deg) brightness(88%) contrast(92%);
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
