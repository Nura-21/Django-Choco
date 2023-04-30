<template>
  <section
    class="category-container flex flex-col self-center mt-10"
    style="width: 80vw"
  >
    <h2 class="font-bold text-xl text-[#4a4b4d]">Заведения</h2>
    <div
      class="flex flex-wrap"
      v-if="$store.foodData.restList && $store.foodData.restList.length"
    >
      <div
        class="w-[350px] h-[220px] mr-[30px] mb-[30px] flex flex-col transition-all hover:transition-all hover:scale-[1.01] cursor-pointer relative"
        v-for="(rest, index) of $store.foodData.restList"
        @click="$router.push({ name: 'restaurant', params: { id: rest.id } })"
        :key="index"
      >
        <img
          :src="rest.img"
          class="w-[350px] h-[170px] rounded-[8px] object-cover"
        />
        <span
          class="absolute bg-white w-[50px] h-[25px] text-[14px] !text-[#f5a623] bottom-[45px] rounded-tr-[13px] pr-[3px] pl-[5px]"
          ><i class="fas fa-star pr-[2px]"></i>{{ rest.rating }}</span
        >
        <span class="w-[100%] font-bold text-xl text-[#4a4b4d]">
          {{ rest.title }}
        </span>
        <span class="flex align-center mt-[6px]">
          <svg
            data-v-26fecbb0=""
            height="18"
            viewBox="0 0 25 18"
            width="25"
            xmlns="http://www.w3.org/2000/svg"
            class="icon pr-[5px]"
          >
            <g data-v-26fecbb0="" fill="#85888b" fill-rule="evenodd">
              <path
                data-v-26fecbb0=""
                d="M4.505 16.144c-.896 0-1.622-.714-1.622-1.595 0-.88.726-1.595 1.622-1.595.896 0 1.622.714 1.622 1.595s-.726 1.595-1.622 1.595m.006-4.092c-1.4 0-2.533 1.116-2.533 2.492 0 1.375 1.134 2.49 2.533 2.49s2.533-1.115 2.533-2.49c0-1.376-1.134-2.492-2.533-2.492"
              ></path>
              <path
                data-v-26fecbb0=""
                d="M22.033 16.066c-.977 0-1.77-.777-1.77-1.735 0-.959.793-1.736 1.77-1.736s1.769.777 1.769 1.736c0 .958-.792 1.735-1.77 1.735m1.322-4.11l.112-.017 1.036.09-1.072-.998c-.363-.339-1.544-1.14-1.544-1.14S19.798 6.88 19.38 6.38c-.417-.499-.254-.695-.327-1.033-.072-.339-.526-.838-.89-1.283-.363-.446-.58-.374-1.07-.463-.491-.09-.346-.838-.346-.838s.164-.338.236-.82c.073-.48-.09-.765-.236-.98-.145-.213-.29-.106-.436 0-.145.108-.236.375-.254.98-.018.606.508.891.545 1.034.036.143-.037.588-.037.588l1.708 6.556-1.653 4.472-3.832-.196s-1.29-3.332-1.435-3.777c-.145-.445.037-.73.2-1.265.164-.534.309-.445.545-.962.236-.517-.2-1.051-.2-1.051s-1.453-.018-2.16.053c-.71.072-1.454-.035-2.398-.07-.944-.037-1.18-.197-2.197-.34-1.017-.142-1.471.108-1.471.108L2.4 8.519l.781 1.621-2.47 1.942 3.051-1.71s.927.41 1.272.605c.345.196.635.428 1.162 1.052.527.623 2.36 1.799 2.36 1.799s2.289 1.318 3.524 1.639c1.235.32 3.723.053 4.485 0 .763-.053.781-.25 1.036-.517.254-.267 1.325-1.567 1.689-2.03.2-.255.465-.418.775-.519a2.677 2.677 0 0 0-.817 1.923c0 1.497 1.237 2.71 2.763 2.71 1.526 0 2.763-1.213 2.763-2.71a2.702 2.702 0 0 0-1.42-2.368"
              ></path>
            </g>
          </svg>
          <span class="text-[#4a4b4d] text-[14px]">{{
            rest.delivery_price
          }}</span>
        </span>
      </div>
    </div>
    <div
      class="self-center text-[#4a4b4d] text-[18px] p-[26px] rounded-[10px] border-[1px]"
      v-else
    >
      Нету совпадений
    </div>
  </section>
</template>

<script>
export default {
  name: "FoodRestList",
};
</script>
