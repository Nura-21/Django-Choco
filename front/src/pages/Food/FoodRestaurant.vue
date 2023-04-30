<template>
  <section class="page flex justify-center mt-[5vh] mb-[5vh]">
    <aside class="w-[50vw] flex flex-col mr-[1vw] relative">
      <img
        :src="$store.foodData.rest.img"
        class="h-[320px] rounded-[5px] object-cover mb-[4vh]"
      />
      <h2 class="text-[#4a4b4d] text-[28px] pl-[2vw]">
        {{ $store.foodData.rest.title }}
      </h2>
      <v-tabs v-model="tab" fixed-tabs>
        <v-tab value="menu">Меню</v-tab>
        <v-tab value="delivery">Доставка</v-tab>
        <v-tab value="review">Отзывы</v-tab>
      </v-tabs>
      <section v-if="tab === 'menu'" class="flex">
        <v-list class="w-[150px]">
          <v-list-item
            v-for="(category, index) of $store.foodData.rest.categories"
            :key="index"
          >
            {{ category.title }}
          </v-list-item>
        </v-list>
        <div class="flex flex-wrap ml-[20px] mt-[20px]">
          <div
            class="flex flex-col w-[250px] h-[360px] mr-[15px] mb-[15px] rounded-[4px] pr-[10px] pl-[10px]"
            style="
              box-shadow: 2px 2px 8px rgb(0 0 0 / 24%),
                2px 2px 6px rgb(0 0 0 / 25%);
            "
            v-for="(product, index) of $store.foodData.rest.products"
            :key="index"
          >
            <img :src="product.img" class="w-full h-[140px] object-cover" />
            <span class="text-[#4a4a4a] text-[14px] font-bold mt-[6px]">{{
              product.title
            }}</span>
            <span class="text-[#9b9b9b] text-[12px] mt-[14px] truncate">{{
              product.description
            }}</span>
            <span class="text-[#4a4a4a] text-[20px] mt-[14px]"
              >{{ product.price }} ₸</span
            >
            <food-green-button
              @click="$store.addFoodProduct($route.params.id, product)"
              class="!w-full !h-[40px] !mt-[50px]"
              text="Добавить в корзину"
            ></food-green-button>
          </div>
        </div>
      </section>
      <section v-if="tab === 'delivery'" class="flex flex-col mt-[30px]">
        <h2 class="text-[16px] text-[#4a4b4d]">
          Стоимость доставки: {{ $store.foodData.rest.delivery_price }} ₸
        </h2>
        <h2 class="text-[16px] text-[#4a4b4d] mt-[20px]">
          Доставка осуществляется курьерами ресторана.
        </h2>
      </section>
      <section v-if="tab === 'review'" class="flex flex-col mt-[30px]">
        <div class="flex align-center gap-[20px]">
          <v-text-field
            v-model="review"
            variant="solo"
            placeholder="Ваш отзыв"
            :rules="[(v) => !!v || 'Поле не может быть пустым']"
          >
          </v-text-field>
          <v-rating
            v-model="rating"
            color="yellow"
            empty-icon="far fa-star"
            full-icon="fas fa-star"
            hover
          ></v-rating>
          <v-btn
            color="blue"
            @click="
              $store.makeReview($route.params.id, review, rating);
              rating = 5;
              review = null;
            "
            >Оставить отзыв</v-btn
          >
        </div>
        <div
          v-if="
            $store.foodData.rest.reviews && $store.foodData.rest.reviews.length
          "
          class="mt-[30px] flex flex-wrap gap-[20px]"
        >
          <v-card
            class="w-fit border-[1px]"
            v-for="(review, index) of $store.foodData.rest.reviews"
            :key="index"
            :title="`${review.creator.first_name} ${review.creator.last_name}`"
            :text="review.comment"
            prepend-icon="fas fa-user"
          >
            <v-rating
              v-model="review.rate"
              :disabled="true"
              color="yellow"
              empty-icon="far fa-star"
              full-icon="fas fa-star"
              size="x-small"
            ></v-rating>
          </v-card>
        </div>
      </section>
    </aside>
    <aside class="w-[20vw]">
      <v-card class="rounded-[6px] shadow">
        <v-card-title
          class="bg-[#d0021b] text-[#FFF] flex align-center justify-between"
          >Корзина
          <span class="text-[12px] underline cursor-pointer"
            >Очистить корзину</span
          >
        </v-card-title>
        <v-card-text>
          <div
            v-if="
              $store.foodCart &&
              $store.foodCart[$route.params.id] &&
              $store.foodCart[$route.params.id].length
            "
            class="flex flex-col"
          >
            <div
              v-for="(product, index) of $store.foodCart[$route.params.id]"
              :key="index"
              class="mt-[10px] h-[80px] flex flex-col justify-between border-b-[1px] pb-[10px]"
            >
              <span class="flex justify-between"
                >{{ product.title }}
                <i
                  class="fas fa-times text-[18px] cursor-pointer"
                  @click="
                    $store.foodCart[$route.params.id].splice(
                      $store.foodCart[$route.params.id].findIndex(
                        (i) => i.id === product.id
                      ),
                      1
                    )
                  "
                ></i>
              </span>
              <div class="flex justify-between">
                <span class="w-[120px] flex justify-between gap-[6px]">
                  <v-btn
                    @click="
                      product.count === 1
                        ? $store.foodCart[$route.params.id].splice(
                            $store.foodCart[$route.params.id].findIndex(
                              (i) => i.id === product.id
                            ),
                            1
                          )
                        : product.count--
                    "
                    icon="fas fa-minus"
                    class="text-[12px] p-[2px]"
                    size="xs-small"
                  ></v-btn>
                  <span
                    class="rounded-[20px] border-[1px] w-full text-center"
                    >{{ product.count }}</span
                  >
                  <v-btn
                    @click="product.count++"
                    icon="fas fa-plus"
                    class="text-[12px] p-[2px]"
                    size="xs-small"
                  ></v-btn>
                </span>
                <span>{{ product.price * product.count }} ₸</span>
              </div>
            </div>
            <div class="mt-[10px] text-[16px]">
              <span class="flex justify-between mb-[10px]">
                <span>Доставка</span>
                <span>{{ $store.foodData.rest.delivery_price }} ₸</span>
              </span>
              <span class="flex justify-between">
                <span>Сумма </span>
                <span
                  >{{
                    $store.getFoodCartSum($route.params.id) +
                    $store.foodData.rest.delivery_price
                  }}
                  ₸</span
                >
              </span>
            </div>
            <food-green-button
              @click="$store.makeOrder($route.params.id)"
              class="!w-full !mt-[30px]"
              text="Оформить заказ"
            ></food-green-button>
          </div>
          <span
            class="flex align-center justify-center mt-[10px] text-[16px] text-[#4a4b4d] border-[1px] rounded-[10px] h-[50px]"
            v-else
          >
            Корзина пуста
          </span>
        </v-card-text>
      </v-card>
    </aside>
  </section>
</template>

<script>
import { useRoute } from "vue-router";
import { useStore } from "@/store";
import { ref } from "vue";

export default {
  name: "FoodRestaurant",
  setup() {
    const store = useStore();
    const route = useRoute();
    const tab = ref(null);
    const review = ref("");
    const rating = ref(5);

    const initPage = async () => {
      store.isLoading = true;
      if (
        store.foodCart &&
        !Object.keys(store.foodCart).find((i) => i === route.params.id)
      ) {
        store.foodCart[route.params.id] = [];
      }
      await store.getRest(route.params.id);
      store.isLoading = false;
    };

    initPage();

    return {
      tab,
      review,
      rating,
    };
  },
};
</script>
