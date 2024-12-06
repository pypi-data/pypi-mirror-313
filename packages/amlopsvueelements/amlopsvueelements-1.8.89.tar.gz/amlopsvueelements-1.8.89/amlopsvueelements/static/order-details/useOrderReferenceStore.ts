import { computed, type Ref, ref, shallowRef } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { useDebounceFn } from '@vueuse/core';
import { defineStore } from 'pinia';
import { useFetch } from 'shared/composables';
import { useMutationOrderPricing, useMutationOrderRoi } from '@/services/mutations';
import { useMutationUpliftOrderPricing } from '@/services/mutations/uplift';
import { useFetchOrderPricing, useFetchSupplyFuel } from '@/services/order/fetchers';
import OrderReferences from '@/services/order/order-references';
import { getUpdateOrderPricingPayload, getUpdateUpliftPricingPayload } from '@/helpers/pricing';
import { getUpdateOrderRoiPayload } from '@/helpers/roi';
import { DEFAULT_ORDER_ROI, DEFAULT_ORDER_ROI_DAYS } from '@/constants/order.constants';
import { useOrderStore } from './useOrderStore';

import type {
  IFuelPricingObj,
  IOrder,
  IOrderRoi,
  IRoiDays,
  IUpliftFuelPricing,
  SelectedSupplierInfo
} from 'shared/types';

export const useOrderReferenceStore = defineStore('OrderReference', () => {
  const orderStore = useOrderStore();
  const orderId = computed(() => orderStore.orderId);
  const selectedSupplierIndex = shallowRef<number | null>(null);
  const selectedSupplierInfo = shallowRef<SelectedSupplierInfo | null>(null);
  const orderPricing: Ref<IFuelPricingObj | null> = ref(null);
  const orderRoi: Ref<IOrderRoi> = ref(DEFAULT_ORDER_ROI);
  const orderRoiDays: Ref<IRoiDays> = ref(DEFAULT_ORDER_ROI_DAYS);
  const queryClient = useQueryClient();

  const { mutate: mutateOrderPricing, isPending: isLoadingUpdateOrderPricing } =
    useMutationOrderPricing();
  const { mutate: mutateUpliftOrderPricing, isPending: isLoadingUpdateUpliftOrderPricing } =
    useMutationUpliftOrderPricing();
  const { mutate: mutateOrderRoi, isPending: isLoadingUpdateOrderRoi } = useMutationOrderRoi();

  const onUpdateOrderRoi = async () => {
    const payload = getUpdateOrderRoiPayload(orderStore.order, orderRoiDays, orderPricing);
    await mutateOrderRoi(
      {
        orderId: orderId.value,
        payload
      },
      {
        onSuccess: (data) => {
          orderRoi.value = data && typeof data === 'object' ? data : DEFAULT_ORDER_ROI;
        }
      }
    );
  };

  const onUpdateOrderPricing = async (updateRoi = false) => {
    await mutateOrderPricing(
      {
        orderId: orderId.value,
        payload: getUpdateOrderPricingPayload(orderPricing, orderRoiDays)
      },
      {
        onSuccess: (data) => {
          if (data && typeof data === 'object') orderPricing.value = data;
          if (updateRoi) onUpdateOrderRoi();
        }
      }
    );
  };

  const onUpdateUpliftOrderPricing = async (
    upliftId: number,
    amount: number | null,
    upliftPricing: IUpliftFuelPricing,
    updateRoi = false
  ) => {
    await mutateUpliftOrderPricing(
      {
        orderId: orderId.value,
        payload: getUpdateUpliftPricingPayload(upliftId, amount, upliftPricing, orderRoiDays)
      },
      {
        onSuccess: (data) => {
          if (data && typeof data === 'object') {
            queryClient.invalidateQueries({ queryKey: ['upliftFuelPricings', orderId.value] });
          }
          if (updateRoi) onUpdateOrderRoi();
        }
      }
    );
  };

  const { callFetch: fetchQuoteButton, data: quoteButton } = useFetch(
    OrderReferences.fetchOrderQuoteButton.bind(OrderReferences)
  );

  const {
    data: supplyFuel,
    callFetch: fetchSupplierFuel,
    loading: isLoadingSupplyFuel
  } = useFetchSupplyFuel();

  const { callFetch: fetchOrderPricing, loading: isLoadingOrderPricing } = useFetchOrderPricing({
    onSuccess: (data: IFuelPricingObj) => {
      orderPricing.value = data;
      const supplierIndex =
        supplyFuel.value?.results?.findIndex(
          (supplier: any) =>
            supplier.supplier.pk === data.supplier_id && supplier.key === data.result_key.toString()
        ) ?? null;

      if (supplierIndex !== -1) {
        selectedSupplierIndex.value = supplierIndex;

        if (supplierIndex !== null && supplyFuel.value) {
          selectedSupplierInfo.value = {
            supplierId: supplyFuel.value?.id,
            detailsId: Number(supplyFuel.value?.results[supplierIndex]?.key)
          };
        }
      }

      orderRoiDays.value.client_days = data.terms_days?.client_terms_days;
      orderRoiDays.value.supplier_days = data.terms_days?.supplier_terms_days;
      if (
        orderStore?.order?.id &&
        orderRoiDays.value.client_days >= 0 &&
        orderRoiDays.value.supplier_days
      ) {
        onUpdateOrderRoi();
      }
    }
  });

  const onSelectSupplier = (supplierInfo: SelectedSupplierInfo) => {
    selectedSupplierInfo.value = supplierInfo;
  };

  const onRoiChange = useDebounceFn((nextValue: string, isClient) => {
    const numValue = parseInt(nextValue);
    if (isClient) {
      orderRoiDays.value.client_days = numValue;
    } else {
      orderRoiDays.value.supplier_days = numValue;
    }
    if (nextValue && orderStore.order?.id) {
      onUpdateOrderRoi();
      onUpdateOrderPricing();
    }
  }, 200);

  const initiateReferenceStore = async (
    orderId: number,
    orderPricingCalculationRecord: IOrder['pricing_calculation_record']
  ) => {
    await Promise.allSettled([
      fetchQuoteButton(orderId),
      fetchSupplierFuel(orderPricingCalculationRecord)
    ]);
  };

  return {
    fetchOrderPricing,
    fetchSupplierFuel,
    initiateReferenceStore,
    fetchQuoteButton,
    isLoadingSupplyFuel,
    isLoadingOrderPricing,
    isLoadingUpdateOrderPricing,
    isLoadingUpdateUpliftOrderPricing,
    isLoadingUpdateOrderRoi,
    onRoiChange,
    onSelectSupplier,
    onUpdateOrderPricing,
    onUpdateUpliftOrderPricing,
    onUpdateOrderRoi,
    orderPricing,
    orderRoi,
    orderRoiDays,
    quoteButton,
    selectedSupplierIndex,
    selectedSupplierInfo,
    supplyFuel
  };
});
