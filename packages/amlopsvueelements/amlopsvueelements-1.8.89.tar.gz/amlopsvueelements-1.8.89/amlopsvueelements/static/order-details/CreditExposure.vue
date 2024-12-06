<template>
  <div v-if="isLoading || !creditExposure" class="w-full flex flex-col items-center">
    <Loading v-if="isLoading" class="py-[1.25rem]" />
    <div
      v-if="!isLoading && !creditExposure"
      class="w-full flex credit-missing justify-center py-[1.25rem]"
    >
      <span>No credit exposure data available</span>
    </div>
  </div>
  <div v-else class="px-[0.75rem] pb-[1rem]">
    <div
      v-if="message"
      class="credit-message py-[0.25rem] px-[0.75rem] flex items-center gap-2 w-fit"
    >
      <img width="20" height="20" src="../../assets/icons/info-circle.svg" alt="warn" />{{
        message
      }}
    </div>
    <div class="credit-wrap flex w-full pt-[2.25rem]">
      <div
        class="credit-confirmed w-full flex flex-col gap-4"
        :style="{ width: calculateWidth(confirmed), display: confirmed === 0 ? 'none' : 'flex' }"
      >
        <div class="credit-confirmed-graph"></div>
        <div class="credit-confirmed-value pl-[0.5rem]">
          <div class="credit-confirmed-value-name">Confirmed Fuel Uplift</div>
          ${{ addThousandSeparators(confirmed.toString()) }}
        </div>
      </div>
      <div
        class="credit-open w-full flex flex-col gap-4"
        :style="{ width: calculateWidth(open), display: open === 0 ? 'none' : 'flex' }"
      >
        <div class="credit-open-graph"></div>
        <div class="credit-open-value pl-[0.5rem]">
          <div class="credit-open-value-name">Open Fuel Releases (Maximum)</div>
          ${{ addThousandSeparators(open.toString()) }}
        </div>
      </div>
      <div
        class="credit-maximum w-full flex flex-col gap-4"
        :class="{ 'no-overuse': overuse === 0 }"
        :style="{
          width: calculateWidth(maximum),
          display: isOpenRelease || maximum === 0 ? 'none' : 'flex'
        }"
      >
        <div class="credit-maximum-graph"></div>
        <div class="credit-maximum-value pl-[0.5rem]">
          <div class="credit-maximum-value-name">Uplift Exposure (Maximum)</div>
          ${{ addThousandSeparators(maximum.toString()) }}
        </div>
        <div
          v-if="overuse === 0 && !isOpenRelease"
          class="credit-maximum-popup px-[0.75rem] py-[0.25rem]"
        >
          Total Credit Exposure (Maximum):
          <span>${{ addThousandSeparators(use.toString()) }}</span>
          <div class="credit-maximum-popup-line"></div>
          <div class="credit-maximum-popup-dot"></div>
        </div>
        <div v-else-if="!isOpenRelease" class="credit-maximum-popup px-[0.75rem] py-[0.25rem]">
          Credit Limit:
          <span>${{ addThousandSeparators(limit.toString()) }}</span>
          <div class="credit-maximum-popup-line"></div>
          <div class="credit-maximum-popup-dot"></div>
        </div>
      </div>
      <div
        v-if="overuse === 0"
        class="credit-remaining w-full flex flex-col gap-4"
        :style="{ width: calculateWidth(remaining) }"
      >
        <div class="credit-remaining-graph"></div>
        <div class="credit-remaining-value pl-[0.5rem]">
          <div class="credit-remaining-value-name">Credit Remaining</div>
          ${{ addThousandSeparators(remaining.toString()) }}
        </div>
        <div class="credit-remaining-popup px-[0.75rem] py-[0.25rem]">
          Credit Limit:
          <span>${{ addThousandSeparators(limit.toString()) }}</span>
          <div class="credit-remaining-popup-line"></div>
          <div class="credit-remaining-popup-dot"></div>
        </div>
      </div>
      <div
        v-else
        class="credit-overuse w-full flex flex-col gap-4"
        :style="{ width: calculateWidth(overuse) }"
      >
        <div class="credit-overuse-graph"></div>
        <div class="credit-overuse-value pl-[0.5rem]">
          <div class="credit-overuse-value-name">Credit Overuse</div>
          ${{ addThousandSeparators(overuse.toString()) }}
        </div>
        <div class="credit-overuse-popup px-[0.75rem] py-[0.25rem]">
          Total Credit Exposure (Maximum):
          <span>${{ addThousandSeparators(capacity.toString()) }}</span>
          <div class="credit-overuse-popup-line"></div>
          <div class="credit-overuse-popup-dot"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue';
import { useOrderStore } from '@/stores/useOrderStore';
import { useFetchCreditExposure } from '@/services/order/fetchers';
import { addThousandSeparators } from '@/helpers/order';
import Loading from '../forms/Loading.vue';

const orderStore = useOrderStore();

const maximum = computed(() => creditExposure.value?.uplift_exposure_max ?? 0);
const confirmed = computed(() => creditExposure.value?.confirmed_unpaid_fuel_uplifts_total ?? 0);
const open = computed(() => creditExposure.value?.open_fuel_release_max_total ?? 0);
const limit = computed(() => creditExposure.value?.client_credit_limit ?? 0);
const remaining = computed(() => creditExposure.value?.remaining_credit ?? 0);
const use = computed(() => maximum.value + confirmed.value + open.value);
const overuse = computed(() => {
  const value = limit.value - (maximum.value + confirmed.value + open.value);
  return value > 0 ? 0 : Math.abs(value);
});
const message = computed(() => creditExposure.value?.remaining_credit_status ?? '');
const capacity = computed(() => limit.value + overuse.value);

const isOpenRelease = computed(() => orderStore.order?.fuel_order?.is_open_release ?? false);

const calculateWidth = (value: number) => {
  const width = (value / capacity.value) * 100;
  return width === 0 || width < 33 ? '33%' : width + '%';
};

const {
  data: creditExposure,
  callFetch: fetchCreditExposure,
  loading: isLoading
} = useFetchCreditExposure();

watch(
  () => [orderStore.order?.id, orderStore.currentStep, orderStore.order?.type?.is_fuel],
  ([id, step, isFuel]) => {
    id && step === 2 && isFuel && fetchCreditExposure(+id);
  }
);
</script>

<style lang="scss">
.credit {
  &-wrap {
    padding-top: 28px;
    background: rgb(245, 246, 249);
    border-radius: 4px 4px 0 0;
  }

  &-missing {
    background-color: rgba(246, 248, 252, 1);

    span {
      color: rgba(82, 90, 122, 1);
      font-size: 11px;
      font-weight: 500;
    }
  }

  &-confirmed {
    background-color: rgb(255, 255, 255);

    &-value {
      border-left: 4px solid rgba(98, 132, 254, 1);
      color: theme('colors.main');
      font-size: 18px;
      font-weight: 600;

      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 12px;
        font-weight: 400;
      }
    }

    &-graph {
      height: 40px;
      width: 100%;
      background-color: rgba(98, 132, 254, 1);
      border-radius: 4px 0 0 4px;
    }
  }

  &-open {
    background-color: rgb(255, 255, 255);

    &-value {
      border-left: 4px solid rgba(243, 173, 43, 1);
      color: theme('colors.main');
      font-size: 18px;
      font-weight: 600;

      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 12px;
        font-weight: 400;
      }
    }

    &-graph {
      height: 40px;
      width: 100%;
      background-color: rgba(243, 173, 43, 1);
    }
  }

  &-maximum {
    background-color: rgb(255, 255, 255);
    position: relative;

    &-value {
      border-left: 4px dashed rgba(254, 98, 98, 1);
      color: theme('colors.main');
      font-size: 18px;
      font-weight: 600;

      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 12px;
        font-weight: 400;
      }
    }

    &-graph {
      height: 40px;
      width: 100%;
      background: repeating-linear-gradient(
        120deg,
        rgba(254, 98, 98, 1),
        rgba(254, 98, 98, 1) 1px,
        rgb(223, 243, 231) 0,
        rgb(223, 243, 231) 12px
      );
    }

    &.no-overuse {
      .credit-maximum-value {
        border-left: 4px dashed rgba(243, 173, 43, 1);
      }

      .credit-maximum-graph {
        background: repeating-linear-gradient(
          120deg,
          rgba(243, 173, 43, 1),
          rgba(243, 173, 43, 1) 1px,
          rgb(223, 243, 231) 0,
          rgb(223, 243, 231) 12px
        );
      }
    }

    &-popup {
      width: max-content;
      position: absolute;
      right: 0;
      top: -14px;
      color: rgba(39, 44, 63, 1);
      font-size: 12px;
      font-weight: 400;
      background: rgba(255, 255, 255, 1);
      border: 1px solid rgba(139, 148, 178, 1);
      border-radius: 4px 4px 0px 4px;

      span {
        font-size: 14px;
        font-weight: 600;
      }

      &-line {
        position: absolute;
        width: 1px;
        right: -1px;
        height: 100%;
        background-color: rgba(139, 148, 178, 1);
      }

      &-dot {
        position: absolute;
        z-index: 1;
        width: 5px;
        right: -3px;
        height: 5px;
        top: 50px;
        border-radius: 50%;
        background-color: rgba(139, 148, 178, 1);
      }
    }
  }

  &-remaining {
    position: relative;
    background-color: rgb(255, 255, 255);

    &-value {
      border-left: 4px solid rgb(223, 243, 231);
      color: theme('colors.main');
      font-size: 18px;
      font-weight: 600;

      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 12px;
        font-weight: 400;
      }
    }

    &-graph {
      height: 40px;
      width: calc(100% + 1px);
      background-color: rgb(223, 243, 231);
    }

    &-popup {
      position: absolute;
      width: max-content;
      right: -1px;
      top: -48px;
      color: rgba(39, 44, 63, 1);
      font-size: 12px;
      font-weight: 400;
      background: rgba(255, 255, 255, 1);
      border: 1px solid rgba(139, 148, 178, 1);
      border-radius: 4px 4px 0px 4px;

      span {
        font-size: 14px;
        font-weight: 600;
      }

      &-line {
        position: absolute;
        width: 1px;
        top: 28px;
        right: -1px;
        height: 59px;
        background-color: rgba(139, 148, 178, 1);
      }

      &-dot {
        position: absolute;
        width: 5px;
        right: -3px;
        height: 5px;
        top: 84px;
        border-radius: 50%;
        background-color: rgba(139, 148, 178, 1);
      }
    }
  }

  &-overuse {
    position: relative;
    background-color: rgb(255, 255, 255);

    &-value {
      border-left: 4px solid rgba(254, 98, 98, 0.12);
      color: rgba(254, 98, 98, 1);
      font-size: 18px;
      font-weight: 600;

      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 12px;
        font-weight: 400;
      }
    }

    &-graph {
      height: 40px;
      width: calc(100% + 1px);
      background: repeating-linear-gradient(
        120deg,
        rgba(254, 98, 98, 1),
        rgba(254, 98, 98, 1) 1px,
        rgb(254, 236, 236) 0,
        rgb(254, 236, 236) 12px
      );
      background-color: rgba(254, 98, 98, 0.12);
      border-radius: 0 4px 4px 0;
    }

    &-popup {
      position: absolute;
      width: max-content;
      right: -1px;
      top: -48px;
      color: rgba(39, 44, 63, 1);
      font-size: 12px;
      font-weight: 400;
      background: rgba(255, 255, 255, 1);
      border: 1px solid rgba(139, 148, 178, 1);
      border-radius: 4px 4px 0px 4px;

      span {
        font-size: 14px;
        font-weight: 600;
        color: rgba(254, 98, 98, 1);
      }

      &-line {
        position: absolute;
        width: 1px;
        top: 28px;
        right: -1px;
        height: 59px;
        background-color: rgba(139, 148, 178, 1);
      }

      &-dot {
        position: absolute;
        width: 5px;
        right: -3px;
        height: 5px;
        top: 84px;
        border-radius: 50%;
        background-color: rgba(139, 148, 178, 1);
      }
    }
  }

  &-message {
    border: 1px solid rgba(139, 148, 178, 1);
    border-radius: 4px;
    color: rgba(39, 44, 63, 1);
    font-size: 15px;
    font-weight: 400;
  }
}
</style>
