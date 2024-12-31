<template>
    <div class="container d-flex justify-content-center align-items-center mt-5">
        <div class="col-md-4 d-inline-block p-4 bg-white bg-opacity-75 rounded shadow">
            <div class="card p-4 bg-white bg-opacity-75">
                <h1 class="card-title">Login</h1>
                <form @submit.prevent="Login">
                    <div class="form-group p-2">
                        <select v-model="user_type" name="user_type" class="form-select" aria-label="Default select example" style="background-color: #a5f2f2;">
                            <option selected value="influencer" style="background-color: #ffffff;">Influencer</option>
                            <option value="sponsor" style="background-color: #ffffff;">Sponsor</option>
                            <option value="admin" style="background-color: #ffffff;">Admin</option>
                          </select>
                    </div>
                    <div class="form-group p-2">
                        <label for="username" class="card-text">Username</label>
                        <input v-model="username" type="text" name="username" class="form-control" required>
                    </div>
                    <div class="form-group p-2">
                        <label for="password" class="card-text">Password</label>
                        <input v-model="password" type="password" name = "password" class="form-control" required>
                    </div>
                    <div v-if="successMessage" class="alert alert-info">
                        {{ successMessage }}
                    </div>
                    <div v-if="errorMessage" class="alert alert-danger">
                        {{ errorMessage }}
                    </div>

                    <div class="form-group mt-3 p-2">
                        <button type="submit" class="btn btn-primary">Login</button>
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
            errorMessage: '',
            successMessage: ''
        };
    },
    methods: {
        async Login() {
            try {
                const response = await axios.post('/login', {
                    username: this.username,
                    password: this.password,
                    user_type: this.user_type,
                });
                const {access_token, user, message} = response.data;
                localStorage.setItem('user',JSON.stringify(user));
                this.$store.dispatch('login',{token:access_token,user});
                this.successMessage = message;
                this,this.errorMessage=''
                setTimeout(() => {
                        this.$router.push('/');
                }, 2000);
            } catch (error) {
                if (error.response && error.response.data.redirect) {
                    this.errorMessage = error.response.data.message;
                    this.successMessage=''
                    setTimeout(() => {
                        this.$router.push(error.response.data.redirect); // Redirect to the signup page
                    }, 2000); // Optional delay before redirecting
                } else {
                    this.errorMessage = error.response ? error.response.data.message : "Login Failed. Please try again.";
                    this.successMessage=''
                }
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