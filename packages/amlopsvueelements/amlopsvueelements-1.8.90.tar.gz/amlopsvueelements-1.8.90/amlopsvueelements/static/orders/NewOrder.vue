<template>
  <div class="order-wrapper">
    <AddPersonModal
      ref="clientInput"
      :is-open="isModalOpened"
      name="first-modal"
      @modal-close="closeModal"
      @modal-submit="addNewPerson"
    />
    <OrderForm :is-loading="isLoading" add-default-classes>
      <template #header>
        <img class="logo" :src="getImageUrl(`assets/icons/logo.svg`)" alt="logo" />
        <h2 class="header-text-name text-[1.25rem] font-medium text-grey-1000">Create New Order</h2>
      </template>
      <template v-if="isFirstStep" #content>
        <Stepper
          class="form-stepper"
          :steps="['General Info', 'Order Details']"
          :current-step="1"
        />
        <h5 class="text-[1rem] font-medium">Step 1 of 2</h5>
        <h2 class="text-[1.5rem] font-medium text-grey-1000">General Information</h2>
        <div class="content-wrap flex flex-col">
          <div class="w-11/12">
            <SelectField
              v-model="formModel.type"
              class="w-11/12"
              label-text="Order Type"
              placeholder="Please select order type"
              :disabled="!meta && !isAdmin"
              :errors="validationInfo?.type?.$errors"
              :is-validation-dirty="validationInfo?.$dirty"
              label="name"
              :options="orderTypes"
              :loading="false"
              @update:model-value="changeType"
            />
          </div>
          <div class="w-11/12">
            <SelectColorField
              v-model="formModel.status"
              label-text="Order Status"
              placeholder="Please select order status"
              :disabled="!meta && !isAdmin"
              :errors="validationInfo?.status?.$errors"
              :is-validation-dirty="validationInfo?.$dirty"
              label="name"
              :small-width="true"
              :options="orderStatuses"
              :loading="false"
            />
          </div>
          <div class="w-11/12">
            <SelectEmField
              v-model="formModel.company"
              label-text="AML Selling Company"
              placeholder="Please select company"
              :disabled="!meta && !isAdmin"
              :errors="validationInfo?.company?.$errors"
              :is-validation-dirty="validationInfo?.$dirty"
              label="full_repr"
              :options="companies"
              :loading="false"
            />
          </div>
          <div class="w-11/12">
            <SelectIndicatorField
              v-model="formModel.client"
              label-text="Client"
              indicator-display="Choose Client"
              :indicator-value-obj="formModel.client?.client_status_list ?? null"
              placeholder="Please select client"
              :disabled="!meta && !isAdmin"
              :errors="validationInfo?.client?.$errors"
              :is-validation-dirty="validationInfo?.$dirty"
              label="full_repr"
              :options="clients"
              :loading="false"
            />
          </div>
          <div class="w-11/12 flex items-start">
            <SelectField
              ref="clientInput"
              v-model="formModel.primary_client_contact"
              label-text="Primary Contact"
              placeholder="Please select primary contact"
              :disabled="(!meta && !isAdmin) || !formModel.client"
              :errors="validationInfo?.primary_client_contact?.$errors"
              :is-validation-dirty="validationInfo?.$dirty"
              label="display"
              :options="organisationPeople"
              :loading="false"
            >
              <template #list-header>
                <li class="add-client-list" @click="openModal()">+ Add new contact</li>
              </template>
            </SelectField>
          </div>
          <AirportLocationApiSelectField
            v-model="formModel.location"
            :is-location="true"
            :errors="validationInfo?.location?.$errors"
            :is-validation-dirty="validationInfo?.$dirty"
            label-text="Location"
            placeholder="Please select airport"
          />
          <div class="w-11/12">
            <SelectField
              v-model="formModel.operator"
              label-text="Operator"
              placeholder="Please select operator"
              :disabled="!meta && !isAdmin"
              :errors="validationInfo?.operator?.$errors"
              :is-validation-dirty="validationInfo?.$dirty"
              label="full_repr"
              :options="operators"
              :loading="false"
            />
          </div>
          <div class="w-full flex">
            <div class="w-11/12">
              <MultiselectField
                ref="multiselectFieldRef"
                v-model="airGroupModel"
                group-values="data"
                group-label="group"
                :multiple="true"
                :group-select="true"
                label-text="Aircraft"
                placeholder="Select Aircraft"
                :show-no-result="false"
                :disabled="(!meta && !isAdmin) || !formModel.client"
                :taggable="false"
                :errors="validationInfo?.aircraft?.$errors"
                :is-validation-dirty="validationInfo?.$dirty"
                label="full_repr"
                :options="airGroups"
                track-by="full_repr"
                :close-on-select="false"
              >
              </MultiselectField>
            </div>
            <div class="flex items-center justify-end mt-4 w-1/12">
              <CheckboxField
                v-model="formModel.aircraft_sub_allowed"
                :disabled="(!meta && !isAdmin) || !formModel.client"
                :size="'24px'"
                class="mb-0 mr-[0.25rem]"
              />
              <p class="text-base whitespace-nowrap">Sub</p>
            </div>
          </div>
          <div
            v-show="airGroupModel && airGroupModel.length > 0"
            class="w-11/12 flex flex-col mb-4 gap-2"
          >
            <div
              v-for="(el, index) in airGroupModel"
              :key="index"
              class="aircraft-el flex justify-between pb-1"
            >
              <div class="aircraft-el-body flex flex-col">
                <div class="aircraft-el-body-name">{{ el.registration ?? el.full_repr }}</div>
                <div v-if="el.type" class="aircraft-el-body-sub">{{ el.type.full_repr }}</div>
              </div>
              <img
                class="pr-3 cursor-pointer"
                :src="getImageUrl(`assets/icons/cross.svg`)"
                alt=""
                @click="removeAircraft(index)"
              />
            </div>
          </div>
          <div class="w-11/12">
            <InputField
              v-model="formModel.callsign"
              :is-validation-dirty="validationInfo?.$dirty"
              :errors="validationInfo?.callsign?.$errors"
              label-text="Callsign"
              placeholder="Please enter callsign"
              @keyup="uppercaseCallsign"
            />
          </div>
          <div class="w-11/12">
            <SelectField
              v-model="formModel.flight_type"
              label-text="Operation Type"
              placeholder="Please select operation type"
              :disabled="!meta && !isAdmin"
              :errors="validationInfo?.flight_type?.$errors"
              :is-validation-dirty="validationInfo?.$dirty"
              label="name"
              :options="flightTypes"
              :loading="false"
            />
          </div>
          <div v-show="showFlightType" class="w-11/12 mb-4">
            <Label label-text="Flight Type" :required="false" />
            <Toggle v-model="formModel.is_private" false-value="Commercial" true-value="Private" />
          </div>
          <SelectField
            v-model="formModel.currency"
            class="w-11/12"
            label-text="Currency"
            placeholder="Please select currency"
            :disabled="(!meta && !isAdmin) || !formModel?.type?.is_fuel"
            :errors="validationInfo?.currency?.$errors"
            :is-validation-dirty="validationInfo?.$dirty"
            label="display_name"
            :options="currencies"
            :loading="false"
            :small-width="true"
          />
        </div>
      </template>
      <template v-if="!isFirstStep && formModel?.type?.is_fuel" #content>
        <Stepper
          class="form-stepper"
          :steps="['General Info', 'Order Details']"
          :current-step="2"
        />
        <h5 class="text-[1rem] font-medium">Step 2 of 2</h5>
        <h2 class="text-[1.5rem] font-medium text-grey-1000">Fuel Order Details</h2>
        <div class="w-11/12">
          <SelectField
            v-model="releaseType"
            class="w-11/12"
            label-text="Release Type"
            placeholder="Please select release type"
            :disabled="!meta && !isAdmin"
            :errors="validationInfo?.fuel_order?.release_type?.$errors"
            :is-validation-dirty="validationInfo?.$dirty"
            label="aircraft"
            :options="['Standard', 'Open']"
            :loading="false"
          />
        </div>
        <div v-if="releaseType === 'Standard'" class="w-full flex flex-col">
          <div class="flex items-start w-full mb-4">
            <div class="w-11/12 flex gap-x-3">
              <div class="w-4/12 min-w-[132px]">
                <Label :required="false" label-text="Arrival Date:" class="whitespace-nowrap" />
                <FlatPickr
                  ref="arrivalDateRef"
                  v-model="arrivalDateTime.date"
                  :errors="validationInfo?.fuel_order?.arrival_datetime_utc?.$errors"
                  :is-validation-dirty="validationInfo?.$dirty"
                  :config="{
                    allowInput: true,
                    altInput: true,
                    altFormat: 'Y-m-d',
                    dateFormat: 'Y-m-d'
                  }"
                />
              </div>
              <div class="w-4/12">
                <Label
                  :required="false"
                  label-text="Time:"
                  class="whitespace-nowrap"
                  :class="{'text-disabled': formModel.fuel_order!.arrival_time_tbc}"
                />
                <FlatPickr
                  v-if="formModel.fuel_order!.arrival_time_tbc"
                  v-model="arrivalDateTime.time"
                  placeholder="Time"
                  :errors="validationInfo?.fuel_order?.arrival_datetime_utc?.$errors"
                  :is-disabled="formModel.fuel_order!.arrival_time_tbc"
                  :is-validation-dirty="validationInfo?.$dirty"
                  :config="{
                    altFormat: 'H:i',
                    altInput: true,
                    allowInput: true,
                    noCalendar: true,
                    enableTime: true,
                    time_24hr: true,
                    minuteIncrement: 1
                  }"
                  class="!pr-0"
                />
                <FlatPickr
                  v-else
                  v-model="arrivalDateTime.time"
                  placeholder="Time"
                  :errors="validationInfo?.fuel_order?.arrival_datetime_utc?.$errors"
                  :is-validation-dirty="validationInfo?.$dirty"
                  :config="{
                    altFormat: 'H:i',
                    altInput: true,
                    allowInput: true,
                    noCalendar: true,
                    enableTime: true,
                    time_24hr: true,
                    minuteIncrement: 1
                  }"
                  class="!pr-0"
                />
              </div>
              <div class="w-4/12">
                <Label
                  :required="false"
                  label-text="Timezone:"
                  class="whitespace-nowrap"
                  :class="{'text-disabled': formModel.fuel_order!.arrival_time_tbc}"
                />
                <SelectField
                  v-model="arrivalDateTime.timezone"
                  :options="['Local', 'UTC']"
                  label="label"
                  placeholder="Timezone"
                  class="timezone-select mb-0 re-css"
                  :append-to-body="false"
                  :disabled="formModel.fuel_order!.arrival_time_tbc ?? false"
                />
              </div>
            </div>
            <div class="flex items-center justify-end mt-[2.5rem] w-1/12">
              <CheckboxField
                v-model="formModel.fuel_order!.arrival_time_tbc"
                :size="'24px'"
                class="mb-0 mr-[0.25rem]"
              />
              <p class="text-base whitespace-nowrap">TBC</p>
            </div>
          </div>
          <div class="flex items-start w-full mb-4">
            <div class="w-11/12 flex gap-x-3">
              <div class="w-4/12 min-w-[132px]">
                <Label :required="false" label-text="Departure Date:" class="whitespace-nowrap" />
                <FlatPickr
                  ref="departureDateRef"
                  v-model="departureDateTime.date"
                  :errors="validationInfo?.fuel_order?.departure_datetime_utc?.$errors"
                  :is-validation-dirty="validationInfo?.$dirty"
                  :config="{
                    allowInput: true,
                    altInput: true,
                    altFormat: 'Y-m-d',
                    dateFormat: 'Y-m-d'
                  }"
                />
              </div>
              <div class="flex flex-col w-4/12">
                <Label
                  :required="false"
                  label-text="Time:"
                  class="whitespace-nowrap"
                  :class="{'text-disabled': formModel.fuel_order!.departure_time_tbc}"
                />
                <FlatPickr
                  v-if="formModel.fuel_order!.departure_time_tbc"
                  v-model="departureDateTime.time"
                  placeholder="Time"
                  :is-disabled="formModel.fuel_order!.departure_time_tbc"
                  :errors="validationInfo?.fuel_order?.departure_datetime_utc?.$errors"
                  :is-validation-dirty="validationInfo?.$dirty"
                  :config="{
                    altFormat: 'H:i',
                    altInput: true,
                    allowInput: true,
                    noCalendar: true,
                    enableTime: true,
                    time_24hr: true,
                    minuteIncrement: 1
                  }"
                  class="!pr-0"
                />
                <FlatPickr
                  v-else
                  v-model="departureDateTime.time"
                  placeholder="Time"
                  :errors="validationInfo?.fuel_order?.departure_datetime_utc?.$errors"
                  :is-validation-dirty="validationInfo?.$dirty"
                  :config="{
                    altFormat: 'H:i',
                    altInput: true,
                    allowInput: true,
                    noCalendar: true,
                    enableTime: true,
                    time_24hr: true,
                    minuteIncrement: 1
                  }"
                  class="!pr-0"
                />
              </div>
              <div class="w-4/12">
                <Label
                  :required="false"
                  label-text="Timezone:"
                  class="whitespace-nowrap"
                  :class="{'text-disabled': formModel.fuel_order!.departure_time_tbc}"
                />
                <SelectField
                  v-model="departureDateTime.timezone"
                  :options="['Local', 'UTC']"
                  label="label"
                  placeholder="Timezone"
                  class="timezone-select mb-0 re-css"
                  :append-to-body="false"
                />
              </div>
            </div>

            <div class="flex items-center justify-end mt-[2.5rem] w-1/12">
              <CheckboxField
                v-model="formModel.fuel_order!.departure_time_tbc"
                :size="'24px'"
                class="mb-0 mr-[0.25rem]"
              />
              <p class="text-base whitespace-nowrap">TBC</p>
            </div>
          </div>
          <div class="w-11/12">
            <SelectField
              v-model="formModel.fuel_order!.fuel_category"
              label-text="Fuel Uplift Category"
              placeholder="Please select fuel uplift category"
              :disabled="!meta && !isAdmin"
              :errors="validationInfo?.fuel_order?.fuel_category?.$errors"
              :is-validation-dirty="validationInfo?.$dirty"
              label="name"
              :options="fuelCategories"
              :loading="false"
            />
          </div>
          <div v-if="airGroupModel?.length === 1" class="flex items-start w-11/12">
            <div class="w-full flex gap-x-3">
              <div class="w-6/12">
                <InputField
                  v-model="formModel.fuel_order!.fuel_quantity"
                  :is-validation-dirty="validationInfo?.$dirty"
                  :errors="validationInfo?.fuel_order?.fuel_quantity?.$errors"
                  label-text="Fuel Uplift Quantity"
                  placeholder="Please enter fuel uplift quantity"
                >
                </InputField>
              </div>
              <div class="w-6/12">
                <Label
                  :required="false"
                  label-text="Quantity"
                  class="whitespace-nowrap text-transparent"
                />
                <SelectField
                  v-model="formModel.fuel_order!.fuel_uom"
                  placeholder="Please select fuel uplift units"
                  :disabled="!meta && !isAdmin"
                  :errors="validationInfo?.fuel_order?.fuel_uom?.$errors"
                  :is-validation-dirty="validationInfo?.$dirty"
                  label="description_plural"
                  :options="fuelQuantityUnits"
                  :loading="false"
                />
              </div>
            </div>
          </div>
          <div v-else class="flex flex-col items-start w-11/12">
            <Label :required="false" label-text="Fuel Uplift Quantity" class="whitespace-nowrap" />
            <div
              v-for="(el, index) in orderStore.fuelGroupModel"
              :key="index"
              class="flex flex-col w-full items-start"
            >
              <div class="w-full flex gap-x-3">
                <div class="w-4/12 flex items-center justify-start mb-3">
                  <div class="aircraft-el-body-naame">{{ airGroupModel[index].registration }}</div>
                </div>
                <InputField
                  v-model="el.fuel_quantity"
                  class="w-4/12"
                  :is-validation-dirty="validationInfo?.$dirty"
                  label-text=""
                  placeholder="Please enter fuel uplift quantity"
                >
                </InputField>
                <SelectField
                  class="w-4/12"
                  :model-value="el!.fuel_uom"
                  placeholder="Please select fuel uplift units"
                  :disabled="(!meta && !isAdmin) || index > 0"
                  label="description_plural"
                  :options="fuelQuantityUnits"
                  :loading="false"
                  @update:model-value="changeUom($event)"
                />
              </div>
            </div>
          </div>
          <div class="flex items-start w-full">
            <div class="w-11/12 flex gap-x-3">
              <div class="w-6/12">
                <InputField
                  v-model="formModel.fuel_order!.post_pre_minutes"
                  :is-validation-dirty="validationInfo?.$dirty"
                  :errors="validationInfo?.fuel_order?.post_pre_minutes?.$errors"
                  label-text="Fuel Uplift Time"
                  placeholder="Please enter fuel uplift time"
                >
                  <template #suffix>minutes</template>
                </InputField>
              </div>
              <div class="w-6/12">
                <Label
                  :required="false"
                  label-text="Quantity"
                  class="whitespace-nowrap text-transparent"
                />
                <SelectField
                  v-model="fuelBeforeAfter"
                  placeholder="Please select fuel uplift time"
                  :disabled="!meta && !isAdmin"
                  :errors="validationInfo?.fuel_order?.fueling_on?.$errors"
                  :is-validation-dirty="validationInfo?.$dirty"
                  label="time"
                  :options="['After Arrival', 'Before Departure']"
                  :loading="false"
                />
              </div>
            </div>
          </div>
          <AirportLocationApiSelectField
            v-model="formModel.destination"
            :is-location="false"
            :errors="validationInfo?.destination?.$errors"
            :is-validation-dirty="validationInfo?.$dirty"
            label-text="Destination Airport:"
            placeholder="Please select Destination Airport"
          />
        </div>
        <div v-if="releaseType === 'Open'" class="w-full flex flex-col">
          <div class="flex items-start w-full mb-4">
            <div class="w-11/12 flex gap-x-3">
              <div class="w-6/12 min-w-[132px]">
                <Label :required="false" label-text="Start Date:" class="whitespace-nowrap" />
                <FlatPickr
                  ref="arrivalDateRef"
                  v-model="arrivalDateTime.date"
                  :errors="validationInfo?.fuel_order?.arrival_datetime_utc?.$errors"
                  :is-validation-dirty="validationInfo?.$dirty"
                  :config="{
                    allowInput: true,
                    altInput: true,
                    altFormat: 'Y-m-d',
                    dateFormat: 'Y-m-d'
                  }"
                />
              </div>
              <div v-if="ufn" class="w-6/12">
                <Label
                  :required="false"
                  label-text="End Date:"
                  class="whitespace-nowrap text-disabled"
                />
                <FlatPickr
                  ref="departureDateRef"
                  :is-disabled="true"
                  :placeholder="'&nbsp;'"
                  :config="{
                    allowInput: true,
                    altInput: true,
                    altFormat: 'Y-m-d',
                    dateFormat: 'Y-m-d'
                  }"
                />
              </div>
              <div v-else class="w-6/12">
                <Label :required="false" label-text="End Date:" class="whitespace-nowrap" />
                <FlatPickr
                  ref="departureDateRef"
                  v-model="departureDateTime.date"
                  :errors="validationInfo?.fuel_order?.arrival_datetime_utc?.$errors"
                  :is-validation-dirty="validationInfo?.$dirty"
                  :config="{
                    allowInput: true,
                    altInput: true,
                    altFormat: 'Y-m-d',
                    dateFormat: 'Y-m-d'
                  }"
                />
              </div>
            </div>
            <div class="flex items-center justify-end mt-[2.5rem] w-1/12">
              <CheckboxField v-model="ufn" :size="'24px'" class="mb-0 mr-[0.25rem]" />
              <p class="text-base whitespace-nowrap">UFN</p>
            </div>
          </div>
        </div>
      </template>
      <template v-if="!isFirstStep && formModel?.type?.is_gh" #content>
        <Stepper class="form-stepper" :steps="['General Info', 'Order Details']" />
        <h5 class="text-[1rem] font-medium">Step 2 of 2</h5>
        <h2 class="text-[1.5rem] font-medium text-grey-1000">Ground Handling Order Details</h2>
        <div class="w-11/12">
          <SelectField
            v-model="formModel.gh_order!.mission_type"
            label-text="Mission Type"
            placeholder="Please select mission type"
            :disabled="!meta && !isAdmin"
            :errors="validationInfo?.gh_order?.mission_type?.$errors"
            :is-validation-dirty="validationInfo?.$dirty"
            label="name"
            :options="missionTypes"
            :loading="false"
          />
        </div>
        <div class="flex items-start w-full mb-4">
          <div class="w-11/12 flex gap-x-3">
            <div class="w-4/12 min-w-[132px]">
              <Label :required="false" label-text="Arrival Date:" class="whitespace-nowrap" />
              <FlatPickr
                ref="arrivalDateRef"
                v-model="arrivalDateTime.date"
                :errors="validationInfo?.gh_order?.arrival_datetime_utc?.$errors"
                :is-validation-dirty="validationInfo?.$dirty"
                :config="{
                  allowInput: true,
                  altInput: true,
                  altFormat: 'Y-m-d',
                  dateFormat: 'Y-m-d'
                }"
              />
            </div>
            <div class="w-4/12">
              <Label :required="false" label-text="Time:" class="whitespace-nowrap" />
              <FlatPickr
                v-if="formModel.gh_order!.arrival_time_tbc"
                v-model="arrivalDateTime.time"
                placeholder="Time"
                :is-disabled="formModel.gh_order!.arrival_time_tbc"
                :errors="validationInfo?.gh_order?.arrival_datetime_utc?.$errors"
                :is-validation-dirty="validationInfo?.$dirty"
                :config="{
                  altFormat: 'H:i',
                  altInput: true,
                  allowInput: true,
                  noCalendar: true,
                  enableTime: true,
                  time_24hr: true,
                  minuteIncrement: 1
                }"
                class="!pr-0"
              />
              <FlatPickr
                v-else
                v-model="arrivalDateTime.time"
                placeholder="Time"
                :errors="validationInfo?.gh_order?.arrival_datetime_utc?.$errors"
                :is-validation-dirty="validationInfo?.$dirty"
                :config="{
                  altFormat: 'H:i',
                  altInput: true,
                  allowInput: true,
                  noCalendar: true,
                  enableTime: true,
                  time_24hr: true,
                  minuteIncrement: 1
                }"
                class="!pr-0"
              />
            </div>
            <div class="w-4/12">
              <Label :required="false" label-text="Timezone:" class="whitespace-nowrap" />
              <SelectField
                v-model="arrivalDateTime.timezone"
                :options="['UTC', 'Local']"
                placeholder="Timezone"
                class="timezone-select mb-0 re-css"
                :append-to-body="false"
              />
            </div>
          </div>
          <div class="flex items-center justify-end mt-[2.5rem] w-1/12">
            <CheckboxField
              v-model="formModel.gh_order!.arrival_time_tbc"
              :size="'24px'"
              class="mb-0 mr-[0.25rem]"
            />
            <p class="text-base whitespace-nowrap">TBC</p>
          </div>
        </div>
        <div class="flex items-start w-full mb-4">
          <div class="w-11/12 flex gap-x-3">
            <div class="w-4/12 min-w-[132px]">
              <Label :required="false" label-text="Departure Date:" class="whitespace-nowrap" />
              <FlatPickr
                ref="departureDateRef"
                v-model="departureDateTime.date"
                :errors="validationInfo?.gh_order?.departure_date?.$errors"
                :is-validation-dirty="validationInfo?.$dirty"
                :config="{
                  allowInput: true,
                  altInput: true,
                  altFormat: 'Y-m-d',
                  dateFormat: 'Y-m-d'
                }"
              />
            </div>
            <div class="flex flex-col w-4/12">
              <Label :required="false" label-text="Time:" class="whitespace-nowrap" />
              <FlatPickr
                v-if="formModel.gh_order!.departure_time_tbc"
                v-model="departureDateTime.time"
                placeholder="Time"
                :is-disabled="formModel.gh_order!.departure_time_tbc"
                :errors="validationInfo?.gh_order?.departure_datetime_utc?.$errors"
                :is-validation-dirty="validationInfo?.$dirty"
                :config="{
                  altFormat: 'H:i',
                  altInput: true,
                  allowInput: true,
                  noCalendar: true,
                  enableTime: true,
                  time_24hr: true,
                  minuteIncrement: 1
                }"
                class="!pr-0"
              />
              <FlatPickr
                v-else
                v-model="departureDateTime.time"
                placeholder="Time"
                :errors="validationInfo?.gh_order?.departure_datetime_utc?.$errors"
                :is-validation-dirty="validationInfo?.$dirty"
                :config="{
                  altFormat: 'H:i',
                  altInput: true,
                  allowInput: true,
                  noCalendar: true,
                  enableTime: true,
                  time_24hr: true,
                  minuteIncrement: 1
                }"
                class="!pr-0"
              />
            </div>
            <div class="w-4/12">
              <Label :required="false" label-text="Timezone:" class="whitespace-nowrap" />
              <SelectField
                v-model="departureDateTime.timezone"
                :options="['UTC', 'Local']"
                label="label"
                placeholder="Timezone"
                class="timezone-select mb-0 re-css"
                :append-to-body="false"
              />
            </div>
          </div>

          <div class="flex items-center justify-end mt-[2.5rem] w-1/12">
            <CheckboxField
              v-model="formModel.gh_order!.departure_time_tbc"
              :size="'24px'"
              class="mb-0 mr-[0.25rem]"
            />
            <p class="text-base whitespace-nowrap">TBC</p>
          </div>
        </div>
        <AirportLocationApiSelectField
          v-model="formModel.destination"
          class="w-11/12"
          :is-location="false"
          :is-tbc="formModel.destination === null"
          :errors="validationInfo?.destination?.$errors"
          :is-validation-dirty="validationInfo?.$dirty"
          label-text="Destination Airport:"
          placeholder="Please select Destination Airport"
        />
      </template>
    </OrderForm>
  </div>
</template>

<script lang="ts" setup>
import { computed, onBeforeMount, onMounted, type PropType, type Ref, ref, watch } from 'vue';
import type { BaseValidation } from '@vuelidate/core';
import { storeToRefs } from 'pinia';
import { Label } from 'shared/components';
import { useFetch } from 'shared/composables';
import { useOrderFormStore } from '@/stores/useOrderFormStore';
import { useOrderStore } from '@/stores/useOrderStore';
import { usePersonFormStore } from '@/stores/usePersonFormStore';
import AirportLocationApiSelectField from '@/components/datacomponent/AirportLocationApiSelectField.vue';
import FlatPickr from '@/components/FlatPickr/FlatPickr.vue';
import OrderForm from '@/components/forms/OrderForm.vue';
import OrderReferences from '@/services/order/order-references';
import { getImageUrl, getIsAdmin } from '@/helpers';
import { toUTC } from '@/helpers/order';
import AddPersonModal from '../../modals/AddPersonModal.vue';
import CheckboxField from '../fields/CheckboxField.vue';
import InputField from '../fields/InputField.vue';
import MultiselectField from '../fields/MultiselectField.vue';
import SelectColorField from '../fields/SelectColorField.vue';
import SelectEmField from '../fields/SelectEmField.vue';
import SelectField from '../fields/SelectField.vue';
import SelectIndicatorField from '../fields/SelectIndicatorField.vue';
import Stepper from '../Stepper.vue';
import Toggle from '../Toggle.vue';

import type { IAircraft, IOrderStatus, IOrderType, ITypeReference } from 'shared/types';

defineProps({
  validationInfo: {
    type: Object as PropType<BaseValidation>,
    default: () => null
  },
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  }
});

const multiselectFieldRef = ref(null);

const orderFormStore = useOrderFormStore();
const orderStore = useOrderStore();

const personFormStore = usePersonFormStore();

const { formModel } = storeToRefs(orderFormStore);

const isFirstStep = computed(() => orderStore.isFirstStep);
const isAdmin = ref(getIsAdmin());
const isModalOpened = ref(false);
const clientInput = ref(null);
const clientInfoLoading = ref(true);
const ufn = ref(false);

const airGroups: Ref<any> = ref([]);
const airGroupModel: Ref<any> = ref(null);

const aircraftTypes: Ref<any> = ref([]);

const releaseType = ref('Standard');
const arrivalDateTime = ref({
  date: new Date(new Date().getTime() + 24 * 60 * 60 * 1000).toLocaleDateString('en-CA'),
  time: '',
  timezone: 'Local'
});
const departureDateTime = ref({
  date: new Date(new Date().getTime() + 48 * 60 * 60 * 1000).toLocaleDateString('en-CA'),
  time: '',
  timezone: 'Local'
});
const fuelBeforeAfter = ref('After Arrival');
const clients: any = ref([]);
const operators: any = ref([]);
const companies: any = ref([]);
const currencies: any = ref([
  {
    id: 127,
    code: 'USD',
    name: 'US Dollar',
    name_plural: 'US Dollars',
    symbol: '$',
    division_name: 'Cents',
    division_factor: 100,
    display_name: 'US Dollar (USD)'
  }
]);
const showFlightType: any = ref(true);

let isUpdating = false;

const { data: organisationPeople, callFetch: fetchOrganisationPeople } = useFetch(
  OrderReferences.fetchOrganisationPeople.bind(OrderReferences)
);

const { data: aircrafts, callFetch: fetchAircrafts } = useFetch<IAircraft[]>(async (id: number) => {
  const data = await OrderReferences.fetchAircrafts(id as number);
  if (typeof data === 'object') {
    const typeArr = data.map((el) => {
      return { ...el.type, type: 'AircraftType' };
    });
    const jsonObject = typeArr.map((el) => JSON.stringify(el));
    const uniqueSet = new Set(jsonObject);
    aircraftTypes.value = Array.from(uniqueSet).map((el) => JSON.parse(el));
  }
  return data;
});

const { data: orderTypes, callFetch: fetchOrderTypes } = useFetch(
  OrderReferences.fetchOrderTypes.bind(OrderReferences)
);

const { data: orderStatuses, callFetch: fetchOrderStatuses } = useFetch<IOrderStatus[]>(
  async () => {
    const data = await OrderReferences.fetchOrderStatuses();
    const defaultEl = data.find((el: IOrderStatus) => el.id === 'new_order');
    if (defaultEl) {
      formModel.value.status = defaultEl;
    }
    return data;
  }
);

const { data: fuelCategories, callFetch: fetchFuelCategories } = useFetch(
  OrderReferences.fetchFuelCategories.bind(OrderReferences)
);

const { data: fuelQuantityUnits, callFetch: fetchFuelQuantityUnits } = useFetch(
  OrderReferences.fetchFuelQuantityUnits.bind(OrderReferences)
);

const { data: missionTypes, callFetch: fetchMissionTypes } = useFetch(
  OrderReferences.fetchMissionTypes.bind(OrderReferences)
);

const { callFetch: fetchClients } = useFetch<void>(async (pageNumber: number) => {
  const { clients: res, meta } = await OrderReferences.fetchClients(pageNumber);
  clients.value = [...clients.value, ...res];
  if (meta.pagination.page !== meta.pagination.pages) {
    fetchClients(++meta.pagination.page);
  }
});

const { callFetch: fetchOperators } = useFetch<void>(async (pageNumber: number) => {
  const { operators: res, meta } = await OrderReferences.fetchOperators(pageNumber);
  operators.value = [...operators.value, ...res];
  if (meta.pagination.page !== meta.pagination.pages) {
    fetchOperators(++meta.pagination.page);
  }
});

const { callFetch: fetchCompanies } = useFetch<void>(async (pageNumber: number) => {
  const { companies: res, meta } = await OrderReferences.fetchCompanies(pageNumber);
  companies.value = [...companies.value, ...res];
  if (meta.pagination.page !== meta.pagination.pages) {
    fetchCompanies(++meta.pagination.page);
  }
});

const { data: flightTypes, callFetch: fetchFlightTypes } = useFetch(
  OrderReferences.fetchFlightTypes.bind(OrderReferences)
);

const { callFetch: fetchCurrencies } = useFetch<void>(async (pageNumber: number) => {
  const { currencies: res, meta } = await OrderReferences.fetchCurrencies(pageNumber);
  if (pageNumber === 1 && res) {
    currencies.value = [...res];
  } else {
    currencies.value = [...currencies.value, ...res];
  }
  if (meta.pagination.page !== meta.pagination.pages) {
    fetchCurrencies(++meta.pagination.page);
  }
});

const { callFetch: fetchFuelCapacity } = useFetch(
  OrderReferences.fetchFuelCapacity.bind(OrderReferences)
);

const { data: meta, callFetch: fetchMeta } = useFetch(
  OrderReferences.fetchMeta.bind(OrderReferences)
);

const changeType = (ev: any) => {
  const orderType: IOrderType = { ...ev };
  orderFormStore.updateOrderType(orderType.is_fuel);
  const defaultFuel = fuelCategories.value?.find(
    (el: ITypeReference) => el.name === 'Jet Turbine Fuel'
  );
  if (defaultFuel && formModel.value.type?.is_fuel) {
    formModel.value.fuel_order!.fuel_category = defaultFuel;
  }
  updateDateTime();
};

const updateDateTime = () => {
  if (formModel.value.type?.is_fuel) {
    formModel.value.fuel_order!.departure_datetime_utc = toUTC(
      departureDateTime.value.date,
      formModel.value.fuel_order!.departure_time_tbc ? null : departureDateTime.value.time
    );
    formModel.value.fuel_order!.arrival_datetime_utc = toUTC(
      arrivalDateTime.value.date,
      formModel.value.fuel_order!.arrival_time_tbc ? null : arrivalDateTime.value.time
    );
  } else {
    formModel.value.gh_order!.departure_datetime_utc = toUTC(
      departureDateTime.value.date,
      formModel.value.gh_order!.departure_time_tbc ? null : departureDateTime.value.time
    );
    formModel.value.gh_order!.arrival_datetime_utc = toUTC(
      arrivalDateTime.value.date,
      formModel.value.gh_order!.arrival_time_tbc ? null : arrivalDateTime.value.time
    );
  }
};

const updateReleaseType = async (release: string) => {
  formModel.value.fuel_order!.is_open_release = release === 'Open';

  if (release === 'Open') {
    if (formModel.value.is_any_aircraft) {
      formModel.value.fuel_order!.fuel_quantity = '1000';
      formModel.value.fuel_order!.fuel_uom = {
        id: 1,
        description: 'US Gallon',
        description_plural: 'US Gallons',
        code: 'USG'
      };
    } else {
      const data = await fetchFuelCapacity(
        airGroupModel.value[0]?.type?.id ?? formModel.value.aircraft_type?.id
      );
      if (typeof data === 'object') {
        formModel.value.fuel_order!.fuel_quantity = data?.capacity;
        formModel.value.fuel_order!.fuel_uom = data?.uom;
      }
    }
    formModel.value.destination = null;
    formModel.value.destination_int_dom = null;
    formModel.value.fuel_order!.arrival_datetime_is_local = true;
    formModel.value.fuel_order!.departure_datetime_is_local = true;
    formModel.value.fuel_order!.arrival_time_tbc = true;
    formModel.value.fuel_order!.departure_time_tbc = true;
    formModel.value.fuel_order!.fueling_on = null;
    formModel.value.fuel_order!.post_pre_minutes = null;
  } else {
    updateDateTime();
    updateFuelBeforeAfter(fuelBeforeAfter.value);
  }
};

const updateFuelBeforeAfter = (val: string) => {
  formModel.value.fuel_order!.fueling_on = val === 'After Arrival' ? 'A' : 'D';
};

const changeUom = (value: string) => {
  orderStore.updateFuelGroupModelUOM(value);
};

const openModal = () => {
  isModalOpened.value = true;
  setTimeout(() => {
    const el = document.getElementById('focusField');
    const input = el?.getElementsByTagName('input');
    if (input?.length) {
      input[0]?.focus();
    }
  });
};
const closeModal = () => {
  isModalOpened.value = false;
};

const addNewPerson = async () => {
  const person = await OrderReferences.addNewPerson(personFormStore.mapForm());
  formModel.value.primary_client_contact = person;
};

const mapAircrafts = () => {
  airGroups.value = [
    { group: '', data: [{ type: 'any', full_repr: 'Any Aircraft' }] },
    { group: 'Fleet', data: aircrafts },
    { group: 'Types operated', data: aircraftTypes }
  ];
};

const removeAircraft = (id: number) => {
  airGroupModel.value.splice(id, 1);
};

const uppercaseCallsign = () => {
  formModel.value.callsign = formModel.value.callsign!.toUpperCase();
};

watch(
  () => meta.value,
  (meta) => {
    if (!formModel.value?.client && meta?.organisation) {
      formModel.value.client = meta?.organisation;
    }
  }
);

watch(
  () => formModel.value?.client?.id,
  async (organisationId: number | undefined | null, oldId) => {
    clientInfoLoading.value = true;
    if (oldId) {
      formModel.value.aircraft = null;
      formModel.value.aircraft_type = null;
    }
    if (organisationId) {
      if (formModel.value?.operator?.id) {
        fetchOrganisationPeople(organisationId as any);
        clientInfoLoading.value = false;
      } else {
        await Promise.allSettled([
          fetchOrganisationPeople(organisationId as any),
          fetchAircrafts(organisationId as any)
        ]);
        clientInfoLoading.value = false;
        airGroupModel.value = null;
      }
      return;
    }
  },
  { immediate: true }
);

watch(
  () => formModel.value?.operator?.id,
  async (organisationId: number | undefined | null, oldId) => {
    clientInfoLoading.value = true;
    if (oldId) {
      formModel.value.aircraft = null;
      formModel.value.aircraft_type = null;
    }
    if (organisationId) {
      await Promise.allSettled([fetchAircrafts(organisationId as any)]);
      clientInfoLoading.value = false;
      airGroupModel.value = null;
      return;
    }
  },
  { immediate: true }
);

watch(() => releaseType.value, updateReleaseType);

watch(() => fuelBeforeAfter.value, updateFuelBeforeAfter);

watch(
  [
    () => formModel.value.fuel_order?.departure_time_tbc,
    () => formModel.value.fuel_order?.arrival_time_tbc,
    () => formModel.value.gh_order?.departure_time_tbc,
    () => formModel.value.gh_order?.arrival_time_tbc
  ],
  ([fuel_dep, fuel_arr, gh_dep, gh_arr]) => {
    if (fuel_dep || gh_dep) {
      departureDateTime.value.time = '';
      departureDateTime.value.timezone = 'UTC';
    }
    if (fuel_arr || gh_arr) {
      arrivalDateTime.value.time = '';
      arrivalDateTime.value.timezone = 'UTC';
    }
  }
);

watch(
  [
    () => departureDateTime.value.date,
    () => arrivalDateTime.value.date,
    () => departureDateTime.value.time,
    () => arrivalDateTime.value.time
  ],
  updateDateTime
);

watch(
  () => departureDateTime.value.timezone,
  (value) => {
    formModel.value.type?.is_fuel
      ? (formModel.value.fuel_order!.departure_datetime_is_local = value === 'Local')
      : (formModel.value.gh_order!.departure_datetime_is_local = value === 'Local');
  }
);

watch(
  () => arrivalDateTime.value.timezone,
  (value) => {
    formModel.value.type?.is_fuel
      ? (formModel.value.fuel_order!.arrival_datetime_is_local = value === 'Local')
      : (formModel.value.gh_order!.arrival_datetime_is_local = value === 'Local');
  }
);

watch(
  () => clientInfoLoading.value,
  (loading) => {
    if (!loading) {
      mapAircrafts();
    }
  }
);

watch(
  () => formModel.value.flight_type,
  (value) => {
    if (
      value &&
      (value.code === 'M' || value.code === 'D' || value.code === 'T' || value.code === 'E')
    ) {
      formModel.value.is_private = true;
      showFlightType.value = false;
    } else if (value && (value.code === 'C' || value.code === 'O')) {
      formModel.value.is_private = false;
      showFlightType.value = false;
    } else {
      showFlightType.value = true;
    }
  }
);

watch(
  () => airGroupModel.value,
  (value) => {
    if (!value || value.length === 0) return;
    if (isUpdating) {
      isUpdating = false;
      return;
    }
    const lastAddedValue = value[value.length - 1];

    if (lastAddedValue.type === 'AircraftType') {
      formModel.value.aircraft = null;
      formModel.value.aircraft_type = lastAddedValue;
      formModel.value.is_any_aircraft = false;
      isUpdating = true;
      airGroupModel.value = [lastAddedValue];
      orderStore.updateAirGroupModel([lastAddedValue]);
      (multiselectFieldRef.value as any).deactivate();
    } else if (lastAddedValue.type === 'any') {
      formModel.value.aircraft_type = null;
      formModel.value.aircraft = null;
      formModel.value.is_any_aircraft = true;

      isUpdating = true;
      airGroupModel.value = [
        {
          full_repr: 'Any Aircraft',
          type: 'any'
        }
      ];
      orderStore.updateAirGroupModel([
        {
          full_repr: 'Any Aircraft',
          type: 'any'
        }
      ]);
      (multiselectFieldRef.value as any).deactivate();
    } else {
      formModel.value.aircraft_type = null;
      formModel.value.aircraft = value;
      formModel.value.is_any_aircraft = false;
      if (aircrafts.value && aircrafts.value?.length === 1) {
        (multiselectFieldRef.value as any).deactivate();
      }
      if (
        airGroupModel.value.find(
          (el: any) =>
            el.type === 'any' ||
            el.type === 'AircraftType' ||
            el.type?.id !== lastAddedValue.type?.id
        )
      ) {
        airGroupModel.value = [lastAddedValue];
        orderStore.updateAirGroupModel([lastAddedValue]);
      } else {
        orderStore.updateAirGroupModel(value);
        const fuelValue = [];
        for (let i = 0; i < value.length; i++) {
          fuelValue.push({ fuel_quantity: '', fuel_uom: '' });
        }
        orderStore.updateFuelGroupModel(fuelValue);
      }
    }
  }
);

onBeforeMount(async () => {
  await Promise.allSettled([
    fetchMeta(),
    fetchOrderStatuses(),
    fetchOrderTypes(),
    fetchFuelCategories(),
    fetchMissionTypes(),
    fetchFuelQuantityUnits(),
    fetchClients(1),
    fetchOperators(1),
    fetchFlightTypes(),
    fetchCurrencies(1),
    fetchCompanies(1)
  ]);
});

onMounted(() => {
  updateDateTime();
  updateReleaseType(releaseType.value);
  updateFuelBeforeAfter(fuelBeforeAfter.value);
  formModel.value.currency = currencies.value[0];
});
</script>

<style lang="scss">
.order-wrapper {
  overflow-y: auto;
  border-radius: 0.5rem;
}

.logo {
  position: absolute;
  left: 2.5rem;
  top: 0;

  @media (max-width: 1600px) {
    display: none !important;
  }
}

.add-button {
  @apply flex shrink-0 focus:shadow-none bg-grey-900 mb-0 mt-2 p-2 px-4 ml-2 #{!important};
  border-radius: 0.5rem;
  background: #eff1f6 !important;
  color: rgb(191, 197, 217) !important;
}

.add-client-list {
  @apply p-2 px-4 cursor-pointer #{!important};
  color: rgba(81, 93, 138, 1) !important;

  &:hover {
    background-color: rgba(125, 148, 231, 0.1) !important;
    color: rgb(125, 148, 231) !important;
  }
}

.aircraft-el {
  border-bottom: 1px solid rgba(223, 226, 236, 1);

  img {
    filter: brightness(0) saturate(100%) invert(54%) sepia(96%) saturate(2350%) hue-rotate(322deg)
      brightness(104%) contrast(114%);
  }

  &-body {
    &-name {
      color: rgba(21, 28, 53, 1);
      font-size: 15px;
      font-weight: 600;
    }

    &-sub {
      color: rgba(60, 67, 93, 1);
      font-size: 14px;
      font-weight: 400;
    }
  }
}

.header-text-name {
  @media (max-width: 1025px) {
    padding-left: 0 !important;
  }
}

.form-stepper {
  position: absolute;
  left: 2.5rem;
  top: 7rem;

  @media (max-width: 1600px) {
    position: static;
    margin-bottom: 2rem;
  }
}
</style>
