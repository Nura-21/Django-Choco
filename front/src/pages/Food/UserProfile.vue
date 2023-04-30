<template>
  <section class="page food-profile">
    <aside class="food-profile-left" style="width: 450px">
      <v-form ref="vForm">
        <div>
          <v-text-field
            v-model="$store.user.first_name"
            variant="solo"
            placeholder="Имя пользователя"
            :rules="$store.rules.required"
          ></v-text-field>
          <v-text-field
            v-model="$store.user.phone"
            variant="solo"
            placeholder="Номер телефона"
            v-maska="'+7 (7##) ### ## ##'"
            :rules="$store.rules.required"
          ></v-text-field>
        </div>
        <v-btn
          @click="submitProfileForm"
          color="#4caf50"
          icon="fas fa-save"
          size="small"
        ></v-btn>
      </v-form>

      <v-list>
        <v-list-item
          v-for="item of $store.constants.menuOptions"
          :key="item.id"
          :style="{ 'border-top': item.id === 0 ? '1px solid #eeeeee' : null }"
          style="cursor: pointer"
          :class="{ active: $route.name === item.route }"
        >
          <v-list-item-title
            @click="
              item.id !== 0
                ? $router.push({ name: item.route })
                : $store.logout()
            "
          >
            <i
              v-if="'icon' in item"
              :class="item.icon"
              style="padding-right: 4px"
            ></i>
            {{ item.title }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </aside>
    <aside class="food-profile-right" style="width: 600px">
      <div v-if="$route.name === 'foodOrders'">
        <h3 class="font-bold">Мои заказы</h3>
        <v-list
          v-if="$store.foodData.userOrders && $store.foodData.userOrders.length"
        >
          <v-list-item
            v-for="(order, index) of $store.foodData.userOrders"
            :key="index"
          >
            <!-- {{ order }} -->
            <div
              style="
                padding: 10px 20px;
                border: 1px solid #efefef;
                border-radius: 6px;
                display: flex;
                align-items: center;
                gap: 30px;
                width: fit-content;
              "
            >
              <span
                ><i class="fas fa-store-alt"></i> {{ order.restaurant }}</span
              >
              <span
                >{{ order.total_cost ? order.total_cost : 0 }}
                <i class="fas fa-tenge"></i
              ></span>
              <span
                ><i class="fas fa-clipboard-list"></i> {{ order.status }}</span
              >
              <v-btn
                v-if="order.status === 'Pending'"
                @click="$store.payOrder(order.id)"
                size="small"
                class="!text-[14px]"
                color="green"
                >Оплатить</v-btn
              >
              <v-btn
                v-if="order.status === 'Pending'"
                @click="$store.cancelOrder(order.id)"
                size="small"
                class="!text-[14px]"
                color="red"
                >Отменить</v-btn
              >
            </div>
          </v-list-item>
        </v-list>
        <div
          v-else
          style="
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            font-size: 20px;
            border: 2px solid #efefef;
            padding: 26px;
            border-radius: 10px;
            color: #808080;
            margin-top: 20px;
          "
        >
          <i class="fas fa-times-circle"></i>
          Нет заказов
        </div>
      </div>
      <div v-if="$route.name === 'foodBonuses'">
        <div style="display: flex; justify-content: space-between">
          <h3 class="font-bold">Мои бонусы</h3>
          <span>Накоплено: {{ $store.user.bonuses }} ₸</span>
        </div>
      </div>
      <div v-if="$route.name === 'foodAddresses'">
        <h3 class="font-bold">Мои адреса</h3>
        <v-text-field
          v-model="$store.user.address"
          variant="solo"
          placeholder="Адресс"
          style="margin-top: 20px"
        >
        </v-text-field>
      </div>
      <div v-if="$route.name === 'foodCards'">
        <h3 class="font-bold">Мои карты</h3>
        <v-form ref="cardForm" class="flex flex-col">
          <v-text-field
            v-model="cardNumber"
            v-maska="'####-####-####-####'"
            variant="solo"
            placeholder="Номер карты"
            :rules="[
              (v) =>
                (!!v && v.length === 19) || 'Введите корректный номер карты',
            ]"
          ></v-text-field>
          <v-text-field
            v-model="cardCVV"
            v-maska="'###'"
            variant="solo"
            placeholder="Номер CVV"
            type="password"
            :rules="[
              (v) => (!!v && v.length === 3) || 'Введите корректный номер CVV',
            ]"
          ></v-text-field>
          {{ cardDate }}
          <Datepicker
            v-model="cardDate"
            placeholder="Дата истечения карты"
            model-type="yyyy-MM-dd"
          ></Datepicker>
          <v-btn color="blue" @click="submitCardForm">Сохранить карту</v-btn>
        </v-form>
        <v-list
          v-if="
            $store.foodData.creditCards && $store.foodData.creditCards.length
          "
        >
          <v-list-item
            v-for="(card, index) of $store.foodData.creditCards"
            :key="index"
          >
            {{ index + 1 }}. Номер карты {{ card.card_number }}
            <v-btn size="small" @click="$store.deleteUserCard(card.id)"
              >Удалить карту</v-btn
            >
          </v-list-item>
        </v-list>
        <div
          v-else
          style="
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            font-size: 20px;
            border: 2px solid #efefef;
            padding: 26px;
            border-radius: 10px;
            color: #808080;
            margin-top: 20px;
          "
        >
          <i class="fas fa-times-circle"></i>
          Нет карты
        </div>
      </div>
    </aside>
  </section>
</template>

<script>
import { ref } from "vue";
import { useStore } from "@/store";

export default {
  name: "UserProfile",
  setup() {
    const vForm = ref(null);
    const cardForm = ref(null);
    const store = useStore();
    const cardNumber = ref(null);
    const cardCVV = ref(null);
    const cardDate = ref(null);

    const initProfile = async () => {
      store.isLoading = true;
      await store.getProfileData();
      store.isLoading = false;
    };

    initProfile();

    const submitProfileForm = async () => {
      await vForm.value.validate().then(async (v) => {
        if (v.valid) {
          await store.updateProfile();
        }
      });
    };

    const submitCardForm = async () => {
      await cardForm.value.validate().then(async (v) => {
        if (v.valid) {
          await store.addUserCard(
            cardNumber.value,
            cardCVV.value,
            cardDate.value
          );
          cardNumber.value = "";
          cardCVV.value = "";
          cardDate.value = "";
        }
      });
    };

    return {
      vForm,
      cardForm,
      submitProfileForm,
      cardNumber,
      cardCVV,
      cardDate,
      submitCardForm,
    };
  },
};
</script>
