import axios from 'axios'
import usersModel from '../models/userModel';
export default new class UserService {

    BASE_URL = "http://127.0.0.1:5000";

    getUser(user: any) {
        return axios.get(`${this.BASE_URL}/log-in`, { params: { user: user } });
    }
    createUser(user: any) {
        return axios.post(`${this.BASE_URL}/sign-up`, { params: { user: user } });
    }

}
