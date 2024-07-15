export default class usersModel {
    name!:string
    email!:string
    password!:string
    statements!:boolean

    constructor(name:string,email:string,password:string,statements:boolean) {
        this.name=name;
        this.email=email;
        this.password=password;
        this.statements=statements;
    }
}

