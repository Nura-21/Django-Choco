import { defineStore } from "pinia";
import constants from "@/constants";
import foodConstants from "@/constants/food.js";
import { rules } from "@/constants/rules";
import { jwtDecode, showToaster } from "@/helpers";


export const useStore = defineStore("store", {
  state: () => ({
    constants: constants,
    rules: rules,
    accessToken: null,
    users: [],
    user: {
      city: constants.cities[0],
      address: null,
    },
    foodData: {
      authModal: false,
      userMenu: false,
      categories: [],
      userOrders: [],
      creditCards: [],
      restList: [],
      rest: {},
    },
    eventsData: {
      alert_info: '',
      category: 0,
      company: 0,
      id: 0,
      expiration_date: '',
      img: '',
      title: '',
      use_until_date: '',
      rating: 0
    },
    categoriesList: {},
    certificatesList: {},
    foodSites: foodConstants.sitesList,
    foodCart: {},
    lifeBasket: [],
    isLoading: false,
  }),
  getters: {
    hasLogged: (state) => "id" in state.user && !!state.user.id,
  },
  actions: {
    async initData() {
      const token = localStorage.getItem("accessToken");
      await this.getFoodCategories();
      if (token) {
        await this.updateUser(token);
      }
    },
    async updateUser(token) {
      this.accessToken = token;
      const decoded = jwtDecode(this.accessToken);
      const userData = await this.api.getUser(decoded.user_id);
      this.user = { ...this.user, ...userData };
    },
    async login(userCredentials) {
      try {
        const loginResponse = await this.api.login(userCredentials);
        if ("token" in loginResponse && !!loginResponse.token) {
          localStorage.setItem("accessToken", loginResponse.token);
          await this.updateUser(loginResponse.token);
        }
      } catch (err) {
        console.log(err);
        if ("response" in err) {
          showToaster(
            "error",
            "Пользователь с такими данными не существует",
            2000
          );
        }
      }
    },
    async authUser(email, password, firstName, lastName, phone) {
      const userData = {
        email: email,
        password: password,
        first_name: firstName,
        last_name: lastName,
        phone: phone,
      };
      try {
        await this.api.addUser(userData);
        await this.login({ email: email, password: password });
        showToaster("success", "Пользователь создан успешно", 3000);
      } catch (err) {
        console.log(err);
        if ("response" in err) {
          showToaster("error", "Что то пошло не так", 3000);
        }
      }
    },
    logout() {
      this.user = { city: constants.cities[0], address: null };
      localStorage.removeItem("accessToken");
      this.accessToken = null;
      this.router.push({ name: "home" });
    },
    async updateProfile() {
      try {
        const userProfileData = (({ first_name, phone, email }) => ({
          first_name,
          phone,
          email,
        }))(this.user);
        const { token } = await this.api.updateProfile(userProfileData);
        await this.updateUser(token);
      } catch (err) {
        console.log(err);
        if ("response" in err) {
          showToaster("error", "Что-то пошло не так", 2000);
        }
      }
    },
    async getFoodCategories() {
      const foodCategories = await this.api.getFoodCategories();
      this.foodData.categories = [
        ...foodCategories,
        ...foodCategories,
        ...foodCategories,
        ...foodCategories,
        ...foodCategories,
        ...foodCategories,
      ];
      this.foodData.categories = foodCategories;
    },
    async getEvents() {
      const events = await this.api.getEvents();
      this.eventsData = events;
      this.foodData.categories = foodCategories;
    },
    async getFoodRestList() {
      const restData = await this.api.getFoodRestaurant();
      this.foodData.restList = restData;
    },
    async getRest(id) {
      const restData = await this.api.getFoodRest(id);
      const [{ value: products }, { value: categories }, { value: reviews }] =
        await Promise.allSettled([
          this.api.getFoodRestProducts(id),
          this.api.getFoodRestCategories(id),
          this.api.getReviews(id),
        ]);
      this.foodData.rest = {
        ...restData,
        products: products,
        categories: categories,
        reviews: reviews,
      };
    },
    async getFoodRestaurantByCategory(id) {
      const restData = await this.api.getFoodRestaurantByCategory(id);
      this.foodData.restList = restData;
    },
    addFoodProduct(restId, product) {
      const inCart = this.foodCart[restId].findIndex(
        (i) => i.id === product.id
      );
      if (inCart !== -1) {
        this.foodCart[restId][inCart].count++;
      } else {
        this.foodCart[restId].push({ ...product, count: 1 });
      }
    },
    getFoodCartSum(restId) {
      return this.foodCart[restId].reduce((a, b) => a + b.price * b.count, 0);
    },
    async makeOrder(restId) {
      const orderProducts = this.foodCart[restId].map((product) => {
        return {
          product_id: product.id,
          count: product.count,
        };
      });

      const orderData = {
        restaurant_id: this.foodData.rest.id,
        products: orderProducts,
        destination_address: this.user.address
          ? this.user.address
          : this.user.city,
      };

      await this.api.makeOrder(orderData);
      this.foodCart[restId] = [];
      this.router.push({ name: "chocofood" });
      showToaster("success", 'Перейдите на страницу "Моих заказы"', 3000);
    },
    async payOrder(orderId) {
      if (this.foodData.creditCards.length === 0) {
        showToaster("error", "Нужно привязать карту", 3000);
        return;
      }
      await this.api.payOrder(orderId, {
        credit_card_id: this.foodData.creditCards[0].id,
      });
      await this.getProfileData();
      await this.updateUser(this.accessToken);
    },
    async cancelOrder(orderId) {
      await this.api.cancelOrder(orderId, {
        comment: "Canceled",
      });
      await this.getProfileData();
      await this.updateUser(this.accessToken);
      showToaster("sucess", "Заказ успешно отменен", 3000);
    },
    async addUserCard(cardNumber, cardCvv, date) {
      const creditData = {
        card_number: cardNumber,
        cvv: Number(cardCvv),
        expiration_date: date,
        type: "Visa",
        owner: this.user.id,
      };
      await this.api.addUserCard(creditData);
      await this.getProfileData();
      showToaster("success", "Карта успешно добавлена", 2000);
    },
    async deleteUserCard(id) {
      await this.api.deleteUserCard(id);
      await this.getProfileData();
      showToaster("success", "Карта успешно удалена", 2000);
    },
    async makeReview(restId, comment, rate) {
      if (!comment) {
        showToaster("error", "Заполните отзыв", 3000);
        return;
      }
      this.isLoading = true;
      const reviewData = {
        comment: comment,
        restaurant_id: Number(restId),
        rate: rate,
      };
      await this.api.makeReview(reviewData);
      await this.getRest(restId);
      this.isLoading = false;
    },
    async searchRest(query) {
      const restData = await this.api.searchRestaurants(query);
      this.foodData.restList = restData;
    },
    async getProfileData() {
      try {
        const [{ value: orders }, { value: creditCards }] =
          await Promise.allSettled([
            this.api.getFoodOrders(),
            this.api.getUserCreditCards(),
          ]);
        this.foodData.userOrders = orders;
        this.foodData.creditCards = creditCards;
      } catch (err) {
        console.log(err);
      }
    },
    async getLifeCertificates() {
      this.certificatesList = await this.api.getLifeCertificates();
    },
    async getCategoryEvents(companyId) {
      await this.api.getCategoryEvents({ category_id: companyId }).then(data => this.eventsData = data.map(event => {
        return { ...event, company: this.getEventCompany(event.company), certificates: this.getEventCertificates(event.id) };
      }));
    },
    async getCategories() {
      const categories = await this.api.getCategories();
      this.categoriesList = categories.map(c => ({ ...c, isSelected: c.id === 0 }));
      this.getCompanies();
      this.getLifeCertificates();
      this.getCategoryEvents(categories[0].id);
    },
    async getCompanies() {
      this.lifeCompanies = await this.api.getLifeCompanies();
    },
    getEventCertificates(eventId) {
      return this.certificatesList.filter(cert => cert.event === eventId);
    },
    getEventCompany(companyId) {
      return this.lifeCompanies.find(comp => comp.id === companyId);
    },
    onCategoryClick(categoryId) {
      this.categoriesList = this.categoriesList.map(c => ({ ...c, isSelected: categoryId === c.id }));
      this.getCategoryEvents(categoryId);
    },
    toggleFoodAuthModal() {
      console.log(this.foodData.authModal);
      this.foodData.authModal = !this.foodData.authModal;
    },
  },
});
