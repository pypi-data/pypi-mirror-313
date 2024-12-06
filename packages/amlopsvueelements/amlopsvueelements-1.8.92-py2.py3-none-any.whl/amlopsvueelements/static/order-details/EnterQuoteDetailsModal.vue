<template>
  <div v-if="isOpen" class="order-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes is-modal>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">
                  Enter Ground Handling Quote Details
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
              <div class="form-body-wrapper">
                <div class="w-full flex gap-3">
                  <div class="w-6/12">
                    <SelectField
                      v-model="selectedOption"
                      label-text="Supplier Reference"
                      placeholder="Choose Reason"
                      label="display"
                      :options="[]"
                    />
                  </div>
                  <div class="w-6/12">
                    <SelectField
                      v-model="selectedOption"
                      label-text="Supplier Reference"
                      placeholder="Choose Reason"
                      label="display"
                      :options="[]"
                    />
                  </div>
                </div>

                <div class="w-full flex gap-3">
                  <SelectField
                    v-model="selectedUom"
                    class="w-6/12"
                    label-text="Quotation Currency"
                    placeholder=""
                    label="description_plural"
                    :options="[]"
                  ></SelectField>
                  <div class="flex flex-col w-6/12">
                    <Label
                      :required="false"
                      label-text="Valid From (UTC)"
                      class="whitespace-nowrap"
                    />
                    <FlatPickr
                      ref="departureDateRef"
                      v-model="toDateTime.date"
                      :config="{
                        allowInput: true,
                        altInput: true,
                        altFormat: 'Y-m-d',
                        dateFormat: 'Y-m-d'
                      }"
                    />
                  </div>
                </div>
                <div class="flex items-center justify-start pb-[0.75rem]">
                  <CheckboxField class="mb-0 mr-[0.25rem]" />
                  <p class="text-base whitespace-nowrap font-semibold text-main">Type-Specific?</p>
                </div>
                <div class="flex items-center justify-start pb-[0.75rem] gap-3">
                  <button class="modal-button icon">
                    <img
                      height="20"
                      width="20"
                      :src="getImageUrl('assets/icons/paperclip.svg')"
                      alt="attachment"
                    />
                  </button>
                  <p class="text-base whitespace-nowrap font-semibold text-main">
                    Supplier Fuel Release
                  </p>
                </div>
              </div>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button
            class="modal-button submit"
            :disabled="body.length > 200"
            @click.stop="onValidate()"
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { type PropType, ref, watch } from 'vue';
import OrderForm from '@/components/forms/OrderForm.vue';
import { getImageUrl } from '@/helpers';
import { notify } from '@/helpers/toast';
import FlatPickr from '../FlatPickr/FlatPickr.vue';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import Label from '../forms/Label.vue';

import type { IOrderQuote } from 'shared/types';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  quote: {
    type: [Object, null] as PropType<IOrderQuote | null>,
    default: () => null
  }
});

const emit = defineEmits(['modal-close', 'modal-submit']);

const selectedOption = ref('');
const selectedUom = ref();

const fromDateTime = ref({
  date: new Date(new Date().getTime() + 24 * 60 * 60 * 1000).toLocaleDateString('en-CA'),
  time: '',
  timezone: 'Local'
});
const toDateTime = ref({
  date: new Date(new Date().getTime() + 48 * 60 * 60 * 1000).toLocaleDateString('en-CA'),
  time: '',
  timezone: 'Local'
});

const target = ref(null);

const subject = ref('');
const body = ref('');
// onClickOutside(target, () => emit('modal-close'))

const onValidate = async () => {
  const isValid = true; // Replace with validation if necessary
  if (!isValid) {
    return notify('Error while submitting, form is not valid!', 'error');
  } else {
    emit('modal-submit');
    emit('modal-close');
  }
};

watch(
  () => [props.isOpen],
  ([isOpen]) => {
    console.log(isOpen);
  }
);
</script>
