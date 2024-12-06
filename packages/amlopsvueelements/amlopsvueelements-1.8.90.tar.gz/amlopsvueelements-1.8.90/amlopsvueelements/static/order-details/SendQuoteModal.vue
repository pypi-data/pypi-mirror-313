<template>
  <div v-if="isOpen" class="order-modal quote-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes is-modal>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">
                  Send Ground Handling Quote Request(s)
                </div>
                <button @click.stop="emit('modal-close')">
                  <img
                    width="12"
                    height="12"
                    src="../../assets/icons/cross.svg"
                    alt="delete"
                    class="close"
                  />
                </button>
              </div>
            </template>
            <template #content>
              <ScrollBar>
                <div class="form-body-wrapper">
                  <div class="quote-modal-text">
                    <div class="quote-modal-text-content text-main font-semibold font-size-[15px]">
                      Select ground handler(s) to request a quote
                    </div>
                    <div class="quote-modal-text-description text-subtitle">
                      Please make sure that all required services have been added to the order
                      before sending the quote requests out.
                    </div>
                  </div>
                  <div class="flex flex-col mt-[1.5rem] mb-[0.75rem] pl-[0.5rem] w-full">
                    <div v-for="handler in mappedHandlers" :key="handler.id" class="flex">
                      <div
                        v-if="handler.is_quote_received"
                        class="flex items-center justify-start pb-[1rem]"
                      >
                        <div class="my-0 mr-[0.5rem]">
                          <img
                            width="20"
                            height="20"
                            :src="getImageUrl('assets/icons/quote_checkbox_received.svg')"
                            alt="checkbox"
                          />
                        </div>
                        <div class="checkbox-text flex items-baseline gap-1">
                          <div class="text-base whitespace-nowrap font-semibold text-main">
                            {{ handler.full_repr }}
                          </div>
                          <div class="text-sm whitespace-nowrap text-subtitle">
                            (Quote Received)
                          </div>
                        </div>
                      </div>
                      <div
                        v-if="handler.is_quote_requested"
                        class="flex items-start justify-start pb-[1rem]"
                      >
                        <div class="my-0 mr-[0.5rem]">
                          <img
                            width="20"
                            height="20"
                            :src="getImageUrl('assets/icons/quote_checkbox_requested.svg')"
                            alt="checkbox"
                          />
                        </div>
                        <div class="checkbox-text flex items-baseline gap-2">
                          <div class="text-base whitespace-nowrap font-semibold text-main">
                            {{ handler.full_repr }}
                          </div>
                          <div class="text-sm whitespace-nowrap text-subtitle">
                            (Waiting for Quote)
                          </div>
                        </div>
                      </div>
                      <div
                        v-if="
                          !handler.is_quote_received &&
                          !handler.is_quote_requested &&
                          handler.is_email_input_required
                        "
                        class="flex items-start justify-start pb-[1rem]"
                      >
                        <CheckboxField
                          v-model="handler.isPinned"
                          :size="'20px'"
                          class="mb-0 mt-[1px] mr-[0.25rem]"
                        />
                        <div class="checkbox-text flex flex-col gap-2">
                          <div
                            class="text-base whitespace-nowrap font-semibold text-main relative flex gap-1"
                          >
                            {{ handler.full_repr }}
                            <div
                              v-if="!isValidEmail(handler.email)"
                              class="quote-modal-tooltip-body hover-wrap contents flex items-center"
                            >
                              <img
                                width="16"
                                height="16"
                                src="../../assets/icons/info-circle.svg"
                                alt="warn"
                                class="filter-red"
                              />
                              <div class="quote-modal-tooltip">
                                {{
                                  !handler.email
                                    ? 'Email address missing'
                                    : !isValidEmail(handler.email!)
                                    ? 'Invalid email'
                                    : ''
                                }}
                              </div>
                            </div>
                          </div>
                          <InputField
                            v-if="handler.isPinned"
                            v-model="handler.email"
                            class="mb-0"
                          />
                        </div>
                      </div>
                      <div
                        v-if="
                          !handler.is_quote_received &&
                          !handler.is_quote_requested &&
                          !handler.is_email_input_required
                        "
                        class="flex items-center justify-start pb-[1rem]"
                      >
                        <CheckboxField
                          v-model="handler.isPinned"
                          :size="'20px'"
                          class="my-0 mr-[0.25rem]"
                        />
                        <div class="checkbox-text flex items-center gap-2">
                          <div class="text-base whitespace-nowrap font-semibold text-main">
                            {{ handler.full_repr }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </ScrollBar>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button class="modal-button submit" :disabled="!isValidForm()" @click.stop="onValidate()">
            Send
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { watch } from 'vue';
import { computed } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { onClickOutside } from '@vueuse/core';
import type { PropType, Ref } from 'vue';
import { useOrderStore } from '@/stores/useOrderStore';
import OrderForm from '@/components/forms/OrderForm.vue';
import { useMutationRequestOrderQuote } from '@/services/mutations';
import { isValidEmail } from '@/utils/validation';
import { getImageUrl } from '@/helpers';
import { notify } from '@/helpers/toast';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import InputField from '../forms/fields/InputField.vue';
import ScrollBar from '../forms/ScrollBar.vue';

import type { IOrderQuoteHandler } from 'shared/types';

const props = defineProps({
  isOpen: Boolean,
  handlers: {
    type: Array as PropType<IOrderQuoteHandler[]>,
    default: () => []
  }
});

const emit = defineEmits(['modal-close', 'modal-submit']);
const target = ref(null);

const queryClient = useQueryClient();
const orderStore = useOrderStore();
const orderId = computed(() => orderStore.order?.id);
const { mutate: requestOrderQuoteMutation } = useMutationRequestOrderQuote();

const mappedHandlers: Ref<any[]> = ref([]);

onClickOutside(target, () => emit('modal-close'));

const isValidForm = () => {
  return (
    mappedHandlers.value.filter((value) => value.isPinned).length > 0 &&
    mappedHandlers.value.every((handler) => {
      if (!handler.isPinned || !handler.is_email_input_required) return true;

      return handler.email && isValidEmail(handler.email);
    })
  );
};

const onValidate = async () => {
  const payload = mappedHandlers.value
    .filter((value) => value.isPinned)
    .map((handler) => {
      const mapped: any = {
        handler: handler.id
      };
      if (handler.is_email_input_required) {
        mapped['contact_email'] = handler.email;
      }
      return mapped;
    });

  await requestOrderQuoteMutation(
    {
      orderId: orderId.value!,
      payload: {
        handlers: payload
      }
    },
    {
      onSuccess: () => {
        notify('Quotes sent successfully', 'success');
        queryClient.invalidateQueries({ queryKey: ['orderQuotes', orderId.value] });
        emit('modal-close');
      }
    }
  );
};

watch(
  () => props.handlers,
  () => {
    mappedHandlers.value = props.handlers.map((handler) => {
      return {
        ...handler,
        email: '',
        isPinned: false
      };
    });
  }
);
</script>

<style scoped lang="scss">
.quote-modal {
  &-text {
    &-content {
      font-size: 15px;
    }

    &-description {
      font-size: 12px;
    }
  }

  .hover-wrap {
    &:hover {
      .quote-modal-tooltip {
        display: block;
      }
    }
    .filter-red {
      filter: brightness(0) saturate(100%) invert(46%) sepia(68%) saturate(1603%) hue-rotate(326deg)
        brightness(108%) contrast(100%);
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
    bottom: 1.8rem;
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
  }
}
</style>
