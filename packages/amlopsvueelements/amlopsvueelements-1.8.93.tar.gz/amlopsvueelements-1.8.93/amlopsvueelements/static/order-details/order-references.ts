import Api from '@/services';
import { getIsAdmin } from '@/helpers';
import type {
  AddOrderServiceRequest,
  ConfirmSupplierOrderServiceRequest,
  DeleteOrderServiceRequest,
  RequestOrderQuoteRequest,
  SelectOrderHandlerRequest
} from '../mutations';
import type {
  AddCRMActivityAttachmentRequest,
  AddCRMActivityRequest,
  DeleteCRMActivityAttachmentRequest,
  DeleteCRMActivityRequest,
  UpdateCRMActivityAttachmentRequest,
  UpdateCRMActivityRequest
} from '../mutations/crm-activity';
import type { SendSupplierOrderRequest } from '../mutations/order';

import type {
  IAircraft,
  IAircraftLocations,
  IAircraftTypeEntity,
  IAirport,
  IAirportLocations,
  IClient,
  IClientDocument,
  IClientQuote,
  IClientQuoteAddresses,
  IConversation,
  ICreditExposure,
  ICrmActivity,
  ICrmActivityType,
  IFuelUnit,
  IGroundHandler,
  IHandlingService,
  IOperator,
  IOrder,
  IOrderPerson,
  IOrderQuote,
  IOrderQuoteHandler,
  IOrderRefreshStatus,
  IOrderRoi,
  IOrderService,
  IOrderStatus,
  IOrderType,
  IOrganisation,
  IPaginatedResponse,
  IRecentFlightsResponse,
  IService,
  ISupplierOrderService,
  ITypeReference
} from 'shared/types';
import type { ISupplierFuelDetails } from 'shared/types';
import type { IActivity, IFuelPricingObj, IProceedCompliance, ISupplierFuel } from 'shared/types';

class OrderReferenceService extends Api {
  async fetchOrderStatuses() {
    const { data } = await this.get<IOrderStatus[]>(`api/v1/orders/order_statuses/?search=`);
    return data && typeof data === 'object' ? data : [];
  }

  async fetchOrderStatus(orderId: number) {
    const { data } = await this.get<IOrderRefreshStatus>(
      `api/v1/orders/${orderId}/refresh_status/`
    );
    return data && typeof data === 'object' ? data : null;
  }

  async fetchOrderTypes() {
    const { data } = await this.get<IOrderType[]>(`api/v1/orders/order_types/`);
    return data;
  }

  async fetchOrganisations(search?: string) {
    const {
      data: { results: organisations }
    } = await this.get<IPaginatedResponse<IOrganisation[]>>('api/v1/admin/organisations/', {
      params: { search, 'page[size]': 999 }
    });
    return organisations;
  }

  async fetchOrganisationPeople(organisationId: number) {
    if (!organisationId) return [];
    const url = `api/v1/organisations/${organisationId}/people/`;
    const { data } = await this.get<IOrderPerson[]>(url);
    return data.map((item) => ({
      ...item,
      display: `${item.details.full_name} (${item.jobs[0]?.job_title})`,
      display_email: `${item.details.full_name} ${item.details.contact_email}`
    }));
  }

  async fetchAircraftTypes(organisationId: number) {
    if (getIsAdmin() && !organisationId) return [];
    const url = getIsAdmin()
      ? `api/v1/admin/organisation/${organisationId}/aircraft_types/`
      : `api/v1/organisation/aircraft_types/`;
    const {
      data: { data }
    } = await this.get<{ data: IAircraftTypeEntity[] }>(url);
    return data.map((el) => ({
      ...el,
      full_repr: `${el.attributes.manufacturer} ${el.attributes.model} (${el.attributes.designator})`
    }));
  }

  async fetchAircrafts(organisationId: number) {
    if (!organisationId) return [];
    const url = `api/v1/aircraft/`;
    const { data } = await this.get<IAircraft[]>(url, {
      params: { operator: organisationId }
    });
    return data;
  }

  async fetchAirportLocations(search?: string | number) {
    const {
      data: { results: airports }
    } = await this.get<IPaginatedResponse<IAirport[]>>('api/v1/organisations/', {
      params: {
        search,
        type: 8,
        optional_fields: 'country'
      }
    });
    return airports;
  }

  async fetchFuelQuantityUnits() {
    const { data } = await this.get<IFuelUnit[]>('api/v1/uom/');
    return data;
  }

  async fetchFuelCategories() {
    const { data } = await this.get<ITypeReference[]>('api/v1/fuel_categories/');
    return data;
  }

  async fetchGroundHandlers(airportId: number) {
    const {
      data: { results: handlers }
    } = await this.get<IPaginatedResponse<IGroundHandler[]>>('api/v1/organisations/', {
      params: {
        type: 3,
        gh_location: airportId
      }
    });
    return handlers;
  }

  async fetchClients() {
    const {
      data: { results: clients }
    } = await this.get<IPaginatedResponse<IClient[]>>('api/v1/organisations/', {
      params: {
        type_str: 'client',
        optional_fields: 'client_status_list'
      }
    });
    return clients;
  }

  async fetchOperators() {
    const {
      data: { results: operators }
    } = await this.get<IPaginatedResponse<IOperator[]>>('api/v1/organisations/', {
      params: {
        type_str: 'operator'
      }
    });
    return operators;
  }

  async fetchMissionTypes() {
    const { data } = await this.get<ITypeReference[]>('api/v1/admin/handling_requests/types/');
    return data;
  }

  async fetchPersonTitles() {
    const { data } = await this.get<ITypeReference[]>('api/v1/person_titles/');
    return data;
  }

  async fetchPersonRoles() {
    const { data } = await this.get<ITypeReference[]>('api/v1/person_roles/');
    return data;
  }

  async fetchServices(
    locationId?: string | number,
    organisationId?: string | number,
    codeName?: string
  ) {
    const { data } = await this.get<{ data: IService[] }>('api/v1/handling_services/', {
      params: { organisation_id: organisationId, location_id: locationId, codename: codeName }
    });
    return data.data
      ?.filter((service) => {
        return !(
          service.attributes.is_dla &&
          !service.attributes.is_dla_visible_arrival &&
          !service.attributes.is_dla_visible_departure
        );
      })
      .map((service) => ({
        ...service,
        id: Number(service.id)
      }));
  }

  async fetchMeta() {
    const { data } = await this.get('api/v1/meta/');
    return data;
  }

  async fetchSupplierFuel(
    orderPricingCalculationRecord: IOrder['pricing_calculation_record']
  ): Promise<ISupplierFuel | null> {
    const { data } = await this.get<ISupplierFuel>(
      `api/v1/pricing/supplier_fuel_pricing/${orderPricingCalculationRecord}/`
    );
    return typeof data === 'object' ? data : null;
  }

  async fetchSupplierFuelDetails({
    supplierId,
    detailsId
  }: {
    supplierId: number;
    detailsId: number;
  }): Promise<ISupplierFuelDetails> {
    const { data } = await this.get<ISupplierFuelDetails>(
      `api/v1/pricing/supplier_fuel_pricing/${supplierId}/results/${detailsId}/`
    );
    return data;
  }

  async selectFuelSupplier(orderId: number, payload: any) {
    const { data } = await this.post<any[]>(
      `api/v1/orders/${orderId}/fuel_pricing/from_pricing_record/`,
      payload
    );
    return data;
  }

  async fetchOrderPricing(orderId: number): Promise<IFuelPricingObj> {
    const { data } = await this.get<IFuelPricingObj>(`api/v1/orders/${orderId}/fuel_pricing/`);
    return data;
  }

  async updateOrderPricing(orderId: number, payload: any): Promise<IFuelPricingObj> {
    const { data } = await this.put<IFuelPricingObj>(
      `api/v1/orders/${orderId}/fuel_pricing/`,
      payload
    );
    return data;
  }

  async updateOrderROI(orderId: number, payload: any) {
    const { data } = await this.post<IOrderRoi>(`api/v1/orders/${orderId}/roi/`, payload);
    return data;
  }

  async fetchFlightAirportLocations(id: number): Promise<IAirportLocations> {
    const { data } = await this.post<any>(`api/v1/sfr_tracking/airport_locations/`, {
      handling_request: id.toString()
    });
    return data;
  }

  async fetchFlightAircraftLocations(id: number): Promise<IAircraftLocations> {
    const { data } = await this.post<any>(`api/v1/sfr_tracking/aircraft_locations/`, {
      handling_request: id.toString()
    });
    return data;
  }

  async fetchRecentFlights(orderId: number) {
    const { data } = await this.get<IRecentFlightsResponse>(
      `api/v1/orders/${orderId}/recent_flights/`
    );
    return typeof data === 'object' ? data : null;
  }

  async fetchClientQuoteAddresses(orderId: number) {
    const { data } = await this.get<IClientQuoteAddresses>(
      `api/v1/orders/${orderId}/client_quote_addresses/`
    );
    if (data && typeof data === 'object') {
      const updatedRecepients = data.recipients.map((recipient) => ({
        ...recipient,
        display: `${recipient.name} (${recipient.address})`
      }));
      const updatedSenders = data.senders.map((sender) => ({
        ...sender,
        display: `${sender.name} (${sender.address})`
      }));
      return {
        ...data,
        recipients: updatedRecepients,
        senders: updatedSenders
      };
    }
    return null;
  }

  async fetchHandlingServices(orderId: number) {
    const { data } = await this.get<IHandlingService[]>(
      `api/v1/orders/${orderId}/services/applicable_services/`
    );
    return typeof data === 'object' ? data : null;
  }

  async fetchOrderServices(orderId: number) {
    const { data } = await this.get<IOrderService[]>(`api/v1/orders/${orderId}/services/`);
    return typeof data === 'object' ? data : null;
  }

  async fetchSupplierOrderServices(orderId: number) {
    const { data } = await this.get<ISupplierOrderService[]>(
      `api/v1/orders/${orderId}/supplier_order/services/`
    );
    return typeof data === 'object' ? data : null;
  }

  async confirmSupplierOrderService({ orderId, serviceId }: ConfirmSupplierOrderServiceRequest) {
    const { data } = await this.patch<ISupplierOrderService>(
      `api/v1/orders/${orderId}/supplier_order/services/${serviceId}/`,
      {
        is_confirmed: true
      }
    );
    return data;
  }

  async fetchOrderQuotes(orderId: number) {
    const { data } = await this.get<IOrderQuote[]>(`api/v1/orders/${orderId}/gh_quotes/`);
    return typeof data === 'object' ? data : null;
  }

  async fetchOrderQuoteHandlers(orderId: number) {
    const { data } = await this.get<IOrderQuoteHandler[]>(
      `api/v1/orders/${orderId}/gh_quotes/ground_handlers/`
    );
    return typeof data === 'object' ? data : null;
  }

  async fetchOrderGroundHandlers(orderId: number) {
    const { data } = await this.get<IOrderQuoteHandler[]>(
      `api/v1/orders/${orderId}/ground_handlers/`
    );
    return typeof data === 'object' ? data : null;
  }

  async fetchOrderClientDocuments(orderId: number) {
    const { data } = await this.get<IClientDocument[]>(
      `api/v1/orders/${orderId}/client_documents/`
    );
    return typeof data === 'object' ? data : null;
  }

  async selectOrderHandler(request: SelectOrderHandlerRequest) {
    const { orderId, payload } = request;
    const { data } = await this.patch<IOrderService>(
      `api/v1/orders/${orderId}/select_ground_handler/`,
      payload
    );
    return data;
  }

  async requestOrderQuote(request: RequestOrderQuoteRequest) {
    const { orderId, payload } = request;
    const { data } = await this.post<IOrderQuote[]>(`api/v1/orders/${orderId}/gh_quotes/`, payload);
    return data;
  }

  async fetchActivityLog(orderId: number) {
    const { data } = await this.get<IActivity[]>(`api/v1/orders/${orderId}/activity_log/`);
    return data;
  }

  async fetchCreditExposure(orderId: number) {
    const { data } = await this.get<ICreditExposure>(`api/v1/orders/${orderId}/credit_exposure/`);
    return typeof data === 'object' ? data : null;
  }

  async fetchProceedCompliance(orderId: number) {
    const { data } = await this.get<IProceedCompliance>(
      `api/v1/orders/${orderId}/proceed_to_compliance/`
    );
    return typeof data === 'object' ? data : null;
  }

  async fetchProceedToOrder(orderId: number) {
    const { data } = await this.get<{ order_tab: string }>(
      `api/v1/orders/${orderId}/proceed_to_order/`
    );
    return data;
  }

  async fetchRequestManagementApproval(orderId: number) {
    const { data } = await this.get<{
      detail: string;
    }>(`api/v1/orders/${orderId}/request_management_approval/`);
    return data;
  }

  async fetchOrderConversation(id: number): Promise<IConversation> {
    const { data } = await this.post<IConversation>(
      `api/v1/orders/${id}/create_staff_conversation/`
    );
    return data;
  }

  async fetchOrderCRM(orderId: number) {
    const { data } = await this.get<ICrmActivity[]>(`api/v1/orders/${orderId}/crm_activity/`);
    return data;
  }

  async fetchOrderCRMTypes() {
    const { data } = await this.get<ICrmActivityType[]>(`api/v1/crm_activity_types/`);
    return data;
  }

  async sendQuoteViaEmail(orderId: number, payload: IClientQuote): Promise<any> {
    const { data } = await this.post(`api/v1/orders/${orderId}/send_client_quote/`, payload);
    return typeof data === 'object' ? data : null;
  }

  async addCRMActivity(request: AddCRMActivityRequest) {
    const { orderId, payload } = request;
    const { data } = await this.post<ICrmActivity>(
      `api/v1/orders/${orderId}/crm_activity/`,
      payload
    );
    return data;
  }

  async deleteCRMActivity(request: DeleteCRMActivityRequest) {
    const { orderId, activityId } = request;
    const { data } = await this.delete<ICrmActivity>(
      `api/v1/orders/${orderId}/crm_activity/${activityId}/`
    );
    return data;
  }

  async updateCRMActivity(request: UpdateCRMActivityRequest) {
    const { orderId, activityId, payload } = request;
    const { data } = await this.patch<ICrmActivity>(
      `api/v1/orders/${orderId}/crm_activity/${activityId}/`,
      payload
    );
    return data;
  }

  async addCRMActivityAttachment(request: AddCRMActivityAttachmentRequest) {
    const { orderId, activityId, payload } = request;
    const formData = new FormData();
    formData.append('description', payload.description);
    formData.append('file', payload.file);
    const { data } = await this.post<ICrmActivity>(
      `api/v1/orders/${orderId}/crm_activity/${activityId}/attachment/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    );
    return data;
  }

  async updateCRMActivityAttachment(request: UpdateCRMActivityAttachmentRequest) {
    const { orderId, activityId, attachmentId, payload } = request;
    const formData = new FormData();
    formData.append('description', payload.description);
    const { data } = await this.patch<ICrmActivity>(
      `api/v1/orders/${orderId}/crm_activity/${activityId}/attachment/${attachmentId}/`,
      formData
    );
    return data;
  }

  async deleteCRMActivityAttachment(request: DeleteCRMActivityAttachmentRequest) {
    const { orderId, activityId, attachmentId } = request;
    const { data } = await this.delete<ICrmActivity>(
      `api/v1/orders/${orderId}/crm_activity/${activityId}/attachment/${attachmentId}/`
    );
    return data;
  }

  async updateOrderService(request: AddOrderServiceRequest) {
    const { orderId, handlingServiceId, payload } = request;
    const { data } = await this.patch<IOrderService[]>(
      `api/v1/orders/${orderId}/services/${handlingServiceId}/`,
      payload
    );
    return data;
  }

  async addOrderService(request: AddOrderServiceRequest) {
    const { orderId, payload } = request;
    const { data } = await this.post<IOrderService[]>(
      `api/v1/orders/${orderId}/services/`,
      payload
    );
    return data;
  }

  async createOrderService(request: AddOrderServiceRequest) {
    const { orderId, payload } = request;
    const { data } = await this.post<IOrderService>(
      `api/v1/orders/${orderId}/services/applicable_services/create/`,
      payload
    );
    return data;
  }

  async deleteOrderService(request: DeleteOrderServiceRequest) {
    const { orderId, handlingServiceId } = request;
    const { data } = await this.delete<IOrderService[]>(
      `api/v1/orders/${orderId}/services/${handlingServiceId}/`
    );
    return data;
  }

  async sendSupplierOrderRequest(request: SendSupplierOrderRequest) {
    const { orderId, payload } = request;
    const { data } = await this.post<{ detail: string }>(
      `api/v1/orders/${orderId}/send_supplier_order/`,
      payload
    );

    return data;
  }
}

export default new OrderReferenceService();
