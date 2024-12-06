<template>
  <div id="order-scroll" class="w-full flex justify-center order-details-app-screen overflow-auto">
    <div v-show="order" class="w-full bg-white flex flex-col">
      <OrderHeader ref="headerRef" :order="order!"></OrderHeader>
      <div class="content-wrap flex gap-2 flex-grow">
        <div class="flex-1 flex flex-col items-center gap-2">
          <OrderFuelTabPricing
            v-show="currentStep === 1 && order?.type?.is_fuel"
            :is-loading="loading"
            :order="order!"
          />
          <OrderGhTabHandling
            v-show="currentStep === 1 && order?.type?.is_gh"
            :is-loading="loading"
            :order="order!"
          />
          <OrderTabCompliance
            v-show="currentStep === 2 && order?.type?.is_fuel"
            :is-loading="loading"
            :order="order!"
            :selected-supplier-info="orderReferenceStore.selectedSupplierInfo"
          />
          <OrderGhTabServicing
            v-show="currentStep === 2 && order?.type?.is_gh"
            :is-loading="loading"
            :order="order!"
          />
          <OrderTabOrder
            v-show="currentStep === 3 && order?.type?.is_fuel"
            :is-loading="loading"
            :order="order!"
          />
          <OrderGhTabSPF
            v-show="currentStep === 3 && order?.type?.is_gh"
            :is-loading="loading"
            :order="order!"
          />
          <!-- <div v-else class="w-full rounded-md h-full bg-white justify-center flex">Tab content</div> -->
          <OrderFuelTabSupplierInvoice v-show="currentStep === 4" />
          <OrderCRM />
        </div>
        <OrderSidebar :is-loading="loading" :order="order!" :header-height="height"></OrderSidebar>
      </div>
    </div>
    <div v-show="!order" class="w-full h-full bg-white flex items-center">
      <Loading />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
import { onUpdated } from 'vue';
import { useRoute } from 'vue-router';
import { useOrderReferenceStore } from '@/stores/useOrderReferenceStore';
import { useOrderStore } from '@/stores/useOrderStore';
import Loading from '@/components/forms/Loading.vue';
import OrderCRM from '@/components/sections/OrderCRM.vue';
import OrderFuelTabPricing from '@/components/sections/OrderFuelTabPricing.vue';
import OrderFuelTabSupplierInvoice from '@/components/sections/OrderFuelTabSupplierInvoice.vue';
import OrderGhTabHandling from '@/components/sections/OrderGhTabHandling.vue';
import OrderGhTabServicing from '@/components/sections/OrderGhTabServicing.vue';
import OrderGhTabSPF from '@/components/sections/OrderGhTabSPF.vue';
import OrderHeader from '@/components/sections/OrderHeader.vue';
import OrderSidebar from '@/components/sections/OrderSidebar.vue';
import OrderTabCompliance from '@/components/sections/OrderTabCompliance.vue';
import OrderTabOrder from '@/components/sections/OrderTabOrder.vue';

const route = useRoute();
const loading = ref(true);
const orderStore = useOrderStore();
const order = computed(() => orderStore.order);
const orderReferenceStore = useOrderReferenceStore();
const currentStep = computed(() => orderStore.currentStep);
const headerRef = ref<any | null>(null);
const height = ref(0);

const handleResize = () => {
  const div = headerRef?.value?.header as HTMLElement;
  const rect = div.getBoundingClientRect();
  const visibleHeight = Math.max(0, rect.bottom - Math.max(rect.top, 0));
  height.value = visibleHeight;
};

watch(
  () => orderStore.orderId,
  async (id) => {
    if (id) {
      if (route?.query.tab) orderStore.changeStep(parseInt(route.query.tab as string));

      const order = await orderStore.fetchOrder(id);

      if (order) {
        order.type.is_fuel
          ? await orderReferenceStore.initiateReferenceStore(id, order.pricing_calculation_record)
          : await orderReferenceStore.fetchQuoteButton(id);
      }

      loading.value = false;
    }
  }
);
onMounted(() => {
  window.addEventListener('resize', handleResize);
  document.getElementById('order-scroll')?.addEventListener('scroll', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  document.getElementById('order-scroll')?.removeEventListener('scroll', handleResize);
});

onUpdated(() => {
  handleResize();
});
</script>

<style lang="scss" module>
.ops {
  &-page-wrapper {
    @apply flex justify-between items-center gap-2 mb-4;

    &__btn {
      @apply flex shrink-0 focus:shadow-none text-white bg-grey-900 mb-0 mt-2 p-2 px-4 #{!important};

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
      @apply flex shrink-0 focus:shadow-none text-grey-900 bg-grey-75 mb-0 mt-2 p-2 px-4 #{!important};
    }

    &__content {
      @apply pr-0 sm:pr-4 sm:mr-[-1rem] relative;
    }
  }
}
</style>

<style lang="scss">
.content-wrap {
  background-color: rgba(223, 226, 236, 1);
  justify-content: flex-end;
  padding: 1rem;
}
.order-details-app-screen {
  height: calc(100vh - 74px);
}
</style>
