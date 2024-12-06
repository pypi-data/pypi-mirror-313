<template>
  <div class="w-full flex justify-center">
    <div class="w-full flex flex-col justify-between" :class="[$style['ops-page-wrapper__order']]">
      <NewOrder :is-loading="isLoading" :validation-info="v$?.form" />
      <div
        class="py-[1rem] px-[1.5rem] w-full flex justify-center"
        :class="[$style['ops-page-wrapper__order__btn__wrapper']]"
      >
        <div class="w-full flex flex-row-reverse items-center justify-between max-w-screen-lg">
          <Button
            v-if="orderStore.isFirstStep"
            :class="[$style['ops-page-wrapper__order__btn']]"
            :loading="isLoading"
            :disabled="!orderFormStore.validateFirstStep()"
            @click="orderStore.changeStep()"
          >
            <span>Next step</span>
          </Button>
          <Button
            v-if="!orderStore.isFirstStep"
            :class="[$style['ops-page-wrapper__order__btn']]"
            :loading="isLoading"
            :disabled="!orderFormStore.validateSecondStep()"
            @click="onValidate"
          >
            <span>Create {{ isFuel ? 'Fuel' : 'Ground Handling' }} Order</span>
          </Button>
          <Button
            v-if="!orderStore.isFirstStep"
            :class="[$style['ops-page-wrapper__order__go-back']]"
            @click="orderStore.changeStep()"
          >
            <span>Back</span>
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import useVuelidate from '@vuelidate/core';
import { storeToRefs } from 'pinia';
import { Button } from 'shared/components';
import { useFetch } from 'shared/composables';
import { useOrderFormStore } from '@/stores/useOrderFormStore';
import { useOrderStore } from '@/stores/useOrderStore';
import NewOrder from '@/components/forms/sections/NewOrder.vue';
import order from '@/services/order/order';
import { rules } from '@/utils/rulesForForms';
import { redirectToURL } from '@/helpers';
import { notify } from '@/helpers/toast';

const orderFormStore = useOrderFormStore();
const orderStore = useOrderStore();
const { formModel: orderForm, formErrors } = storeToRefs(orderFormStore);
const validationModel = ref({ form: orderForm.value });
const isFuel = ref(true);

// eslint-disable-next-line prefer-const
let v$ = ref();

const { loading: isCreatingOrder, callFetch: createOrder } = useFetch(async () => {
  const mappedPayload = orderFormStore.mapForm();
  const res = await order.create(mappedPayload);
  notify('Order created successfully!', 'success');
  redirectToURL(res.data?.id);
});

const isLoading = computed(() => isCreatingOrder?.value);

const orderActions = async () => {
  createOrder();
};

const onValidate = async () => {
  try {
    const isValid = await v$?.value?.$validate();
    if (!isValid) {
      const value = JSON.parse(JSON.stringify(v$.value));
      const find = value.$errors.find((el: any) => el.$property === 'status');
      if (find) {
        orderStore.changeStep();
      }
      return notify('Error while submitting, form is not valid!', 'error');
    } else {
      await orderActions();
      formErrors.value = [];
    }
  } catch (error: any) {
    if (error.response?.data?.errors?.some((err: any) => typeof err === 'string')) {
      return (formErrors.value = error.response?.data?.errors);
    }
  }
};

watch(
  () => orderForm.value.type,
  (newVal: any) => {
    isFuel.value = newVal.is_fuel!;
    v$ = ref(useVuelidate(rules(), validationModel));
  }
);
</script>

<style lang="scss" module>
.ops {
  &-page-wrapper {
    @apply flex justify-between items-center gap-2 mb-4;

    &__content {
      @apply pr-0 sm:pr-4 sm:mr-[-1rem] relative;
    }

    &__order {
      height: calc(100vh - 74px);
      background: rgb(255, 255, 255);
      border: 1px solid #e5e7eb;
      border-radius: 0.5rem;

      &__btn {
        @apply flex shrink-0 focus:shadow-none text-white bg-grey-900 p-2 px-4 border-transparent rounded-xl #{!important};

        &__wrapper {
          border-top: 1px solid #e5e7eb;
        }

        img {
          @apply w-5 h-5 mr-2;
          filter: invert(36%) sepia(14%) saturate(1445%) hue-rotate(190deg) brightness(93%)
            contrast(84%);
        }

        &:disabled {
          background-color: rgba(81, 93, 138, 0.5) !important;
        }
      }

      &__go-back {
        @apply flex shrink-0 focus:shadow-none text-grey-900 bg-grey-75 p-2 px-4 border-transparent #{!important};
      }
    }
  }
}
</style>
