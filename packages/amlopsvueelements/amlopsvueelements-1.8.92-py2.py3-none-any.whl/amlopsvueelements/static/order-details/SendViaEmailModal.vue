<template>
  <div v-if="isOpen" class="order-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes is-modal>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">
                  Send Client Quote via Email
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
                  <Label label-text="Recipients" :required="true"></Label>
                  <SelectField
                    v-model="selectedOptions"
                    label-text=""
                    label="display"
                    :options="quoteAddresses?.recipients ?? []"
                    :multiple="true"
                    :disable-delete-first="isDisabledRecipients"
                    required
                  ></SelectField>
                  <SelectField
                    v-model="sender"
                    label-text="From"
                    label="display"
                    :options="quoteAddresses?.senders ?? []"
                    required
                  ></SelectField>
                  <InputField
                    v-model="subject"
                    class="w-full"
                    label-text="Subject"
                    placeholder="Please enter subject"
                    required
                  />
                  <TextareaField
                    v-model="body"
                    class="w-full"
                    label-text="Additional Note"
                    placeholder="Please enter body text"
                  />
                </div>
              </ScrollBar>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button class="modal-button submit" @click.stop="sendViaEmail()">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, type Ref, ref, watch } from 'vue';
import { useOrderStore } from '@/stores/useOrderStore';
import OrderForm from '@/components/forms/OrderForm.vue';
import orderReferences from '@/services/order/order-references';
import { useQueryClientQuoteAddresses } from '@/services/queries';
import { notify } from '@/helpers/toast';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import TextareaField from '../forms/fields/TextareaField.vue';
import Label from '../forms/Label.vue';
import ScrollBar from '../forms/ScrollBar.vue';

import type { IClientQuote, IClientQuoteRecipient, IClientQuoteSender } from 'shared/types';

const props = defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['modal-close', 'modal-submit']);
const orderStore = useOrderStore();
const orderId = computed(() => orderStore.order?.id);
const enabled = ref(false);
const isDisabledRecipients = ref(false);

const selectedOptions: Ref<any> = ref([]);
const sender: Ref<IClientQuoteSender | null> = ref(null);
const primaryContact: Ref<IClientQuoteRecipient | null> = ref(null);

const target = ref(null);

const subject = ref('');
const body = ref('');

const hasError = () => {
  let error = '';
  if (!sender.value?.address) error = 'Error fetching current user email';
  if (!subject.value) error = 'Subject is required';
  if (!selectedOptions.value.length) error = 'At least one recepient is required';
  if (error) notify(error, 'error');
  return error;
};

const sendViaEmail = async () => {
  if (hasError()) return;
  const payload: IClientQuote = {
    subject: subject.value,
    sender: sender.value!.address,
    recipients: selectedOptions.value.map((item: IClientQuoteRecipient) => ({
      address: item.address,
      recipient_type: item.recipient_type
    }))
  };
  if (body.value) {
    payload['notes'] = body.value;
  }
  const send = await orderReferences.sendQuoteViaEmail(orderStore!.order!.id!, payload);
  if (send) {
    orderStore.sendClientQuote(true);
    emit('modal-close');
  }
};

const { data: quoteAddresses } = useQueryClientQuoteAddresses(orderId, { enabled });

watch(
  () => [orderId.value, props.isOpen],
  ([id, isOpen]) => {
    if (id && isOpen) {
      enabled.value = true;
    }
  }
);

watch(
  () => selectedOptions.value,
  (value) => {
    if (primaryContact.value && !value.includes(primaryContact.value)) {
      selectedOptions.value.unshift(primaryContact.value);
    }
  }
);

watch(
  () => quoteAddresses.value,
  (value) => {
    value?.recipients.forEach((person: IClientQuoteRecipient) => {
      if (person.is_primary_contact) {
        selectedOptions.value.push(person);
        isDisabledRecipients.value = true;
        primaryContact.value = person;
      }
    });
    value?.recipients.forEach((person: IClientQuoteRecipient) => {
      if (
        person.is_pre_selected &&
        !selectedOptions.value.some(
          (option: IClientQuoteRecipient) => person.address === option.address
        )
      ) {
        selectedOptions.value.push(person);
      }
    });
    value?.senders.forEach((person: IClientQuoteSender) => {
      if (person.is_pre_selected) {
        sender.value = person;
      }
    });
  }
);
</script>
