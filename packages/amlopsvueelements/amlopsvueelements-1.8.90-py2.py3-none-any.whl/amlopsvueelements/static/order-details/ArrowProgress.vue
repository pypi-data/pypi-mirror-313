<template>
  <div class="arrow-stepper flex w-full justify-around">
    <div
      v-for="(step, key, index) in displaySteps"
      :key="key"
      class="arrow-step cursor-pointer"
      :class="{
        completed: index + 1 < currentStep || (step as IProgressDetails).is_completed,
        current: index + 1 === currentStep,
        disabled: (step as IProgressDetails).is_active
      }"
      :style="{ width: `${100 / Object.keys(displaySteps!).length}%` }"
      @click="orderStore.changeStep(index + 1)"
    >
      <div class="tick"></div>
      <span class="uppercase">{{ (key as string).split('_').join(' ') }}</span>
      <div class="arrow"></div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, type PropType, type Ref, watch } from 'vue';
import { ref } from 'vue';
import { useOrderStore } from '@/stores/useOrderStore';

import type { IFuelProgress, IGhProgress, IProgress, IProgressDetails } from 'shared/types';

const props = defineProps({
  steps: {
    type: [Object, null] as PropType<IProgress | null | undefined>,
    default: () => null
  }
});

const orderStore = useOrderStore();
const order = computed(() => orderStore.order);
const currentStep = computed(() => orderStore.currentStep);
const displaySteps: Ref<IProgress | null | undefined> = ref();

watch(
  () => [props.steps, order.value],
  ([steps, orderValue]) => {
    if (steps && orderValue && order?.value?.type?.is_fuel) {
      displaySteps.value = props.steps;
      const desiredOrder: Array<keyof IFuelProgress> = [
        'pricing',
        'compliance',
        'order',
        'supplier_invoice',
        'client_invoice'
      ];
      const reorderedSteps = {} as IFuelProgress;
      desiredOrder.forEach((key) => {
        if ((props.steps as IFuelProgress)![key]) {
          reorderedSteps[key] = (displaySteps.value as IFuelProgress)![key];
        }
      });
      displaySteps.value = reorderedSteps;
    } else if (steps && orderValue && order?.value?.type?.is_gh) {
      displaySteps.value = props.steps;
      const desiredOrder: Array<keyof IGhProgress> = [
        'ground_handling',
        'servicing',
        'spf',
        'invoicing'
      ];
      const reorderedSteps = {} as IGhProgress;
      desiredOrder.forEach((key) => {
        if ((props.steps as IGhProgress)![key]) {
          reorderedSteps[key] = (displaySteps.value as IGhProgress)![key];
        }
      });
      displaySteps.value = reorderedSteps;
    }
  }
);
</script>
<style lang="scss">
.arrow-stepper {
  .arrow-step {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    color: rgba(133, 141, 173, 1);
    padding: 0.5rem;
    border: 1px solid rgba(223, 226, 236, 1);
    border-left: none;
    border-right: none;
    position: relative;
    font-size: 14px;

    .arrow {
      position: absolute;
      height: 27px;
      width: 27px;
      right: -14px;
      transform: rotate(45deg);
      border-right: 1px solid rgba(223, 226, 236, 1);
      border-top: 1px solid rgba(223, 226, 236, 1);
    }

    &:last-of-type {
      .arrow {
        display: none;
      }
    }

    &.current {
      color: white;
      background-color: rgba(125, 148, 231, 1);
      border-color: rgba(125, 148, 231, 1);

      .arrow {
        z-index: 2;
        background-color: rgba(125, 148, 231, 1);
        border-color: rgba(125, 148, 231, 1);
      }
    }

    &.completed {
      background-color: rgb(225, 243, 239);
      color: rgba(11, 161, 125, 1);
      border-color: rgba(11, 161, 125, 1);

      .arrow {
        z-index: 3;
        background-color: rgb(225, 243, 239);
        border-color: rgba(11, 161, 125, 1);
      }

      .tick {
        height: 20px;
        width: 20px;
        z-index: 1;
        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3e%3cpath fill='none' stroke='%2343c780' stroke-linecap='round' stroke-linejoin='round' stroke-width='3' d='M6 10l3 3l6-6'/%3e%3c/svg%3e");
      }
    }

    &.disabled {
      cursor: default;
    }
  }
}
</style>
