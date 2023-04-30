<template>
  <v-dialog
    class="food-dialog"
    v-model="$store.foodData.authModal"
    width="350"
    :scrollable="false"
  >
    <v-card height="100%">
      <div class="food-dialog-header">
        <h2>Для начала</h2>
        <TimesIcon @click="$store.toggleFoodAuthModal" />
      </div>
      <div class="food-dialog-body">
        <span>Чтобы войти, надо ввести почту и пароль</span>
        <v-form ref="vForm" lazy-validation>
          <v-text-field
            v-model="email"
            label="Почта"
            prepend-inner-icon="fas fa-envelope"
            variant="solo"
            :rules="$store.rules.email"
            @change="validateForm"
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Пароль"
            prepend-inner-icon="fas fa-lock"
            :rules="$store.rules.required"
            variant="solo"
            type="password"
            @change="validateForm"
          ></v-text-field>
          <v-text-field
            v-if="isReg"
            v-model="firstName"
            label="Имя"
            variant="solo"
            :rules="$store.rules.required"
            @change="validateForm"
          ></v-text-field>
          <v-text-field
            v-if="isReg"
            v-model="lastName"
            label="Фамилья"
            variant="solo"
            :rules="$store.rules.required"
            @change="validateForm"
          ></v-text-field>
          <v-text-field
            v-if="isReg"
            v-model="phone"
            v-maska="'+7 (7##) ### ## ##'"
            label="Номер телефона"
            variant="solo"
            :rules="$store.rules.required"
            @change="validateForm"
          ></v-text-field>
        </v-form>

        <small
          v-if="isReg === false"
          class="text-[14px] text-[#4a4b4d] cursor-pointer"
          @click="isReg = true"
          >Зарегистрироваться</small
        >
        <small
          v-if="isReg === true"
          class="text-[14px] text-[#4a4b4d] cursor-pointer"
          @click="isReg = false"
          >Войти</small
        >
        <button
          :class="{ active: isFormValid }"
          @click="submitAuthForm"
          class="food-dialog-btn"
        >
          Далее
        </button>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, watch } from "vue";
import { useStore } from "@/store";

export default {
  name: "AuthDialog",
  setup() {
    const store = useStore();
    const vForm = ref(null);
    const isFormValid = ref(false);
    const email = ref(null);
    const password = ref(null);
    const firstName = ref(null);
    const lastName = ref(null);
    const phone = ref(null);
    const isReg = ref(false);

    watch(
      () => {
        return { email: email.value, password: password.value };
      },
      () => {
        validateForm();
      }
    );

    const validateForm = async () => {
      const { valid } = await vForm.value.validate();
      isFormValid.value = valid;
      return valid;
    };

    const submitAuthForm = async () => {
      await vForm.value.validate().then(async (v) => {
        if (v.valid) {
          if (isReg.value === false) {
            await store.login({ email: email.value, password: password.value });
          } else {
            await store.authUser(
              email.value,
              password.value,
              firstName.value,
              lastName.value,
              phone.value
            );
          }
          if (store.accessToken !== null) {
            store.toggleFoodAuthModal();
            email.value = null;
            password.value = null;
            firstName.value = null;
            lastName.value = null;
            phone.value = null;
          }
        }
      });
    };

    return {
      vForm,
      isFormValid,
      submitAuthForm,
      validateForm,
      email,
      password,
      firstName,
      lastName,
      phone,
      isReg,
    };
  },
};
</script>
