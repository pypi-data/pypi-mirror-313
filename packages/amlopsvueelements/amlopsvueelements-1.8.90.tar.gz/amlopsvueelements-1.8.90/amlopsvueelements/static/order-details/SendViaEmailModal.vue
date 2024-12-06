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
                  <SelectField
                    v-model="selectedOptions"
                    label-text="Recepients"
                    label="display"
                    :options="organisationPeople ?? []"
                    :multiple="true"
                    required
                  ></SelectField>
                  <Label label-text="From" :required="false"></Label>
                  <div class="mb-4">{{ userMeta?.person?.details?.contact_email }}</div>
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
import { type Ref, ref, watch } from 'vue';
import { useFetch } from 'shared/composables';
import { useOrderStore } from '@/stores/useOrderStore';
import OrderForm from '@/components/forms/OrderForm.vue';
import OrderReferences from '@/services/order/order-references';
import orderReferences from '@/services/order/order-references';
import { useQueryUserMeta } from '@/services/queries/user';
import { notify } from '@/helpers/toast';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import TextareaField from '../forms/fields/TextareaField.vue';
import Label from '../forms/Label.vue';
import ScrollBar from '../forms/ScrollBar.vue';

import type { IClientQuote, IOrderPerson } from 'shared/types';

const props = defineProps({
  isOpen: Boolean,
  organisationId: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['modal-close', 'modal-submit']);
const orderStore = useOrderStore();

const selectedOptions: Ref<any> = ref([]);

const target = ref(null);

const { data: userMeta } = useQueryUserMeta();

const subject = ref('');
const body = ref('');

const hasError = () => {
  let error = '';
  if (!userMeta.value?.person?.details?.contact_email) error = 'Error fetching current user email';
  if (!subject.value) error = 'Subject is required';
  if (!selectedOptions.value.length) error = 'At least one recepient is required';
  if (error) notify(error, 'error');
  return error;
};

const sendViaEmail = async () => {
  if (hasError()) return;
  const payload: IClientQuote = {
    subject: subject.value,
    sender: userMeta.value!.person!.details!.contact_email!,
    recipients: selectedOptions.value.map((item: IOrderPerson) => item.id)
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

const { data: organisationPeople, callFetch: fetchOrganisationPeople } = useFetch<IOrderPerson[]>(
  async (id: number) => {
    const data = await OrderReferences.fetchOrganisationPeople(id as number);
    return data;
  }
);

watch(
  () => [props.organisationId, props.isOpen],
  ([id, isOpen]) => {
    id && isOpen && fetchOrganisationPeople(id);
  }
);
</script>
