<template>
  <auth-dialog></auth-dialog>
  <header class="header food-header">
    <section class="food-header-container">
      <div class="header-city">
        <MapIcon />
        <button
          @click="toggleSelect = !toggleSelect"
          class="food-btn food-btn-rounded header-city-btn"
        >
          <v-select
            v-model="$store.user.city"
            :items="$store.constants.cities"
            hide-details
            variant="solo"
          ></v-select>
        </button>
      </div>
      <div class="header-logo">
        <router-link :to="{ name: 'chocofood' }">
          <img
            draggable="false"
            src="https://chocofood.kz/images/chocofood-w.svg"
          />
        </router-link>
      </div>
      <div class="header-login">
        <button
          @click="$store.hasLogged ? null : $store.toggleFoodAuthModal()"
          class="food-btn food-btn-rounded"
        >
          <food-user-menu v-if="$store.hasLogged"></food-user-menu>
          {{ $store.hasLogged ? $store.user.email : "Вход" }}
        </button>
      </div>
    </section>
  </header>
</template>

<script>
import { ref } from "vue";
export default {
  name: "FoodHeader",
  components: {},
  setup() {
    const toggleSelect = ref(false);

    return {
      toggleSelect,
    };
  },
};
</script>
