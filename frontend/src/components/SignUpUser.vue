<template>
    <div class="container d-flex justify-content-center align-items-center mt-5">
        <div class="col-md-4 d-inline-block p-4 bg-white bg-opacity-75 rounded shadow">
            <div class="card p-4 bg-white bg-opacity-75">
                <h1 class="card-title">Sign Up</h1>

                <form @submit.prevent="Signup">
                    <div class="form-group p-2">
                        <select v-model="user_type" name="user_type" id="user_type" class="form-select" aria-label="Default select example" style="background-color: #a5f2f2;">
                            <option value="influencer" style="background-color: #ffffff;">Influencer</option>
                            <option value="sponsor" style="background-color: #ffffff;">Sponsor</option>
                            </select>
                    </div>
                    <div class="form-group p-2">
                        <label for="username" class="card-text">Username</label>
                        <input type="text" name="username" v-model="username" class="form-control" required>
                    </div>
                    <div class="form-group p-2">
                        <label for="password" class="card-text">Password</label>
                        <input type="password" name="password" v-model="password" class="form-control" required>
                    </div>
                    <div class="form-group p-2">
                        <label for="confirm_password" class="card-text">Confirm Password</label>
                        <input type="password" name = "confirm_password" v-model="confirm_password" class="form-control" required>
                    </div>
                    <div class="form-group p-2">
                        <label for="name" class="card-text">Name</label>
                        <input type="text" name="name" v-model="name" class="form-control" required>
                    </div>

                    <!-- Fields for Influencer -->
                    <div v-if="user_type === 'influencer'">
                        <div class="form-group p-2">
                            <label for="category" class="card-text">Category</label>
                            <input type="text" name="category" v-model="category" class="form-control" required>
                        </div>
                        <div class="form-group p-2">
                            <label for="niche" class="card-text">Niche</label>
                            <input type="text" name="niche" v-model="niche" class="form-control" required>
                        </div>
                        <div class="form-group p-2">
                            <label for="reach" class="card-text">Reach</label>
                            <input type="number" name="reach" v-model="reach" class="form-control" min="0" required>
                        </div>
                    </div>

                    <!-- Fields for Sponsor -->
                    <div v-if="user_type === 'sponsor'">
                        <div class="form-group p-2">
                            <label for="budget" class="card-text">Budget</label>
                            <input type="number" name="budget" v-model="budget" class="form-control" min="0" required>
                        </div>
                        <div class="form-group p-2">
                            <label for="industry" class="card-text">Industry</label>
                            <input type="text" name="industry" v-model="industry" class="form-control" required>
                        </div>
                    </div>
                    <div v-if="successMessage" class="alert alert-info">
                        {{ successMessage }}
                    </div>
                    <div v-if="errorMessage" class="alert alert-danger">
                        {{ errorMessage }}
                    </div>

                    <div class="form-group mt-3 p-2">
                        <button type="submit" class="btn btn-primary">Sign Up</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            user_type: 'influencer',
            username: '',
            password: '',
            confirm_password: '',
            name: '',
            category: '',
            niche: '',
            reach: null,
            budget: null,
            industry: '',
            errorMessage: '',
            successMessage: ''
        };
    },
    methods: {
        async Signup() {
            try {
                const response = await axios.post('/signup', {
                    user_type: this.user_type,
                    username: this.username,
                    password: this.password,
                    confirm_password: this.confirm_password,
                    name : this.name,
                    category: this.user_type === 'influencer' ? this.category : null,
                    niche: this.user_type === 'influencer' ? this.niche : null,
                    reach: this.user_type === 'influencer' ? this.reach : null,
                    budget: this.user_type === 'sponsor' ? this.budget : null,
                    industry: this.user_type === 'sponsor' ? this.industry : null
                });
                const {message} = response.data;
                this.successMessage = message;
                setTimeout(() => {
                        this.$router.push('/login');
                }, 2000);
            } catch (error) {
                this.errorMessage = error.response ? error.response.data.message : "Sign Up Failed. Please try again.";
            }
        }
    }
}
</script>


<style scoped>
.container {

min-height: 100vh; /* Make sure the container takes up full viewport height */

}
</style>