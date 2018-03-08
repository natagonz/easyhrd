from flask import Flask , render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from form import UserRegisterForm ,UserLoginForm, AddEmployeForm,AddReviewForm,EditPhotoForm,SuperuserRegisterForm,ForgotPasswordForm,ResetPasswordForm,OwnerRegisterForm,OwnerLoginForm,ConfirmPaymentForm,OwnerEditUserForm,OwnerEditConfirmForm,UserEditAccountForm,AddBlogPostForm,SearchForm,AddKpiForm,AddAttendanceForm,SubmitForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_login import LoginManager , UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_uploads import UploadSet, IMAGES, configure_uploads
from config import database,secret
from functools import wraps
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager 
from sqlalchemy import or_
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,TextAreaField, IntegerField, DateField, SelectField, SubmitField, FloatField
from wtforms.validators import InputRequired, EqualTo, Email, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField



app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = database
app.config["SECRET_KEY"] = secret
db = SQLAlchemy(app)
app.debug = True

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db',MigrateCommand) 




#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "UserLogin"


#fungsi Upload
#mengatur image
images = UploadSet("images",IMAGES)
app.config["UPLOADED_IMAGES_DEST"] = "static/img/profile/"
app.config["UPLOADED_IMAGES_URL"] = "http://127.0.0.1:5000/static/img/profile/"
configure_uploads(app,images)



#fungsi mail
app.config.from_pyfile("config.py") 
mail = Mail(app)
s = URLSafeTimedSerializer("secret")



class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(100))
	email = db.Column(db.String(100))
	phone = db.Column(db.String(100))
	company = db.Column(db.String(100))
	password = db.Column(db.String(100))
	double_pass = db.Column(db.String(400))
	role = db.Column(db.String(100))
	trial_date = db.Column(db.DateTime())
	start_date = db.Column(db.DateTime())
	renew_date = db.Column(db.DateTime())
	status = db.Column(db.String(100))
	users = db.Column(db.Integer())	
	owner = db.relationship("Employe",backref="owner",lazy="dynamic")
	atten = db.relationship("Attendance",backref="atten",lazy="dynamic")
	reviewer = db.relationship("Review",backref="reviewer",lazy="dynamic")
	kpier = db.relationship("Kpi",backref="kpier",lazy="dynamic")
	attener = db.relationship("Attendance",backref="attener",lazy="dynamic")

	def is_active(self):
		return True

	def get_id(self):
		return self.id

	def is_authenticated(self):
		return self.authenticated

	def is_anonymous(self):
		return False



class Employe(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	phone = db.Column(db.String(100))
	departement = db.Column(db.String(100))	
	salary = db.Column(db.String(100))
	added = db.Column(db.DateTime())	
	birth = db.Column(db.DateTime())
	address = db.Column(db.String(100))
	gender = db.Column(db.String(100))
	status = db.Column(db.String(100))
	religion = db.Column(db.String(100))
	notes = db.Column(db.UnicodeText())
	nik = db.Column(db.String(200))
	cabang = db.Column(db.String(200))
	education = db.Column(db.String(200))
	institut =  db.Column(db.String(200))
	jurusan =  db.Column(db.String(200))
	ktp =  db.Column(db.String(200))
	npwp =  db.Column(db.String(200))
	bank =  db.Column(db.String(200))
	bank_account =  db.Column(db.String(200))
	no_rek =  db.Column(db.String(200))
	bpjs_kesehatan =  db.Column(db.String(200))
	bpjs_ketenagakerjaan =  db.Column(db.String(200))	
	owner_id = db.Column(db.Integer(),db.ForeignKey("user.id"))
	image_name = db.Column(db.String(200))
	reviews = db.relationship("Review",backref="reviews",lazy="dynamic")
	kpis = db.relationship("Kpi",backref="kpis",lazy="dynamic")
	attens = db.relationship("Attendance",backref="attens",lazy="dynamic")

	def __repr__(self):
		return '{}'.format(self.name)





class Attendance(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	departement = db.Column(db.String(100))
	start = db.Column(db.DateTime())
	end = db.Column(db.DateTime())
	reason = db.Column(db.UnicodeText())
	status = db.Column(db.String(100))
	attens_id = db.Column(db.Integer(),db.ForeignKey("employe.id"))
	attener_id = db.Column(db.Integer(),db.ForeignKey("user.id"))
	attener_owner = db.Column(db.Integer())
	date = db.Column(db.DateTime())



class Review(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	review = db.Column(db.UnicodeText())
	date = db.Column(db.DateTime())
	posted = db.Column(db.String(100))	
	reviews_id = db.Column(db.Integer(),db.ForeignKey("employe.id"))
	reviewer_id = db.Column(db.Integer(),db.ForeignKey("user.id"))
	reviewer_owner = db.Column(db.Integer())


class Kpi(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	key = db.Column(db.UnicodeText())
	indicator = db.Column(db.String(100))
	target = db.Column(db.Integer())
	complish = db.Column(db.Integer())
	result = db.Column(db.Float())
	date = db.Column(db.DateTime())
	kpis_id = db.Column(db.Integer(),db.ForeignKey("employe.id"))
	kpier_id = db.Column(db.Integer(),db.ForeignKey("user.id"))
	kpier_owner = db.Column(db.Integer())



class Confirm(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(200))
	email = db.Column(db.String(200))
	from_bank = db.Column(db.String(200))
	to_bank = db.Column(db.String(200))
	bank_account = db.Column(db.String(200))
	date = db.Column(db.DateTime()) 	
	status = db.Column(db.String(200))



class Blog(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	date = db.Column(db.DateTime())
	slug = db.Column(db.String(200))
	title = db.Column(db.String(200))
	body = db.Column(db.UnicodeText())
	image = db.Column(db.String(300))






############ wrapper #################
#user loader
@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))


#mengatur role 
def roles_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if ((current_user.role != role) and (role != "ANY")):
                return "no access"
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


###################### Error Handler #########################
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error/500.html")






############### app route ###########################    
@app.route("/")
def Index():
	return render_template("index.html")




##################### admin route #####################
@app.route("/admin-register",methods=["GET","POST"])
def OwnerRegister():
	form = OwnerRegisterForm()
	if form.validate_on_submit():
		hass = generate_password_hash(form.password.data,method="sha256")
		double = generate_password_hash(form.double.data,method="sha256")
		user = User(username=form.username.data,email=form.email.data,password=hass,double_pass=double,role="SuperUser")
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("OwnerLogin"))
	return render_template("admin/register.html",form=form)



@app.route("/yuk-masuk",methods=["GET","POST"])
def OwnerLogin():
	form = OwnerLoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user :
			if check_password_hash(user.password,form.password.data) and check_password_hash(user.double_pass,form.double.data):				
				login_user(user)
				flash("Yuk masuk")
				return redirect(url_for("OwnerDashboard"))
		flash("Someting wrong","danger")
	return render_template("admin/login.html",form=form)	




@app.route("/admin/dashboard",methods=["GET","POST"])
@login_required
@roles_required(role="SuperUser")
def OwnerDashboard():
	users = len(User.query.filter_by(role="user").all())
	trial = len(User.query.filter_by(status="trial").all())
	pending = len(User.query.filter_by(status="pending").all())
	active = len(User.query.filter_by(status="active").all())	
	return render_template("admin/dashboard.html",users=users,trial=trial,pending=pending,active=active)


@app.route("/admin/dashboard/all-user",methods=["GET","POST"])
@login_required
@roles_required(role="SuperUser")
def AllUser():
	users = User.query.filter_by(role="user").all()
	return render_template("admin/users.html",users=users)



@app.route("/admin/dashboard/trial-user",methods=["GET","POST"])
@login_required
@roles_required(role="SuperUser")
def TrialUser():
	users = User.query.filter_by(status="trial").all()
	return render_template("admin/users.html",users=users)


@app.route("/admin/dashboard/pending-user",methods=["GET","POST"])
@login_required
@roles_required(role="SuperUser")
def PendingUser():
	users = User.query.filter_by(status="pending").all()
	return render_template("admin/users.html",users=users)


@app.route("/admin/dashboard/active-user",methods=["GET","POST"])
@login_required
@roles_required(role="SuperUser")
def ActiveUser():
	users = User.query.filter_by(status="active").all()
	return render_template("admin/users.html",users=users)



@app.route("/admin/dashboard/edit-user/<string:id>",methods=["GET","POST"])
@login_required
@roles_required(role="SuperUser")
def OwnerEditUser(id):
	user = User.query.filter_by(id=id).first()
	form = OwnerEditUserForm()		
	form.renew.data = user.renew_date 
	form.status.data = user.status
	if form.validate_on_submit():
		renew = datetime.strptime(request.form["renew"], '%m/%d/%Y').strftime('%Y-%m-%d')	
		user.renew_date = renew
		user.status = request.form["status"] 
		db.session.commit()
		flash("User berhasil di edit","success")
		return redirect(url_for("AllUser"))
	return render_template("admin/edit_user.html",form=form,user=user)	





@app.route("/admin/dashboard/delete-user/<string:id>",methods=["GET","POST"])
@login_required
@roles_required(role="SuperUser")
def OwnerDeleteUser(id):
	user = User.query.filter_by(id=id).first()
	db.session.delete(user)
	db.session.commit()
	flash("User berhasil di hapus","success")
	return redirect(url_for("OwnerDashboard"))



@app.route("/admin/dashboard/confirm",methods=["GET","POST"])
@login_required
@roles_required(role="SuperUser")
def PaymentConfirmFromUser():
	confirms = Confirm.query.all()
	return render_template("admin/all_confirm.html",confirms=confirms)


@app.route("/admin/dashboard/edit-confirm/<string:id>",methods=["GET","POST"])
@login_required
@roles_required(role="SuperUser")
def OwnerEditConfirm(id):	
	form = OwnerEditConfirmForm()
	confirm = Confirm.query.filter_by(id=id).first()
	useremail = confirm.email
	user = User.query.filter_by(email=useremail).first()
	form.status.data = confirm.status
	if form.validate_on_submit():
		status = request.form["status"]
		confirm.status = status
		if status == "paid":
			user.status = "active"
			db.session.commit()
			flash("Status berhasil di perbaharui","success")
			return redirect(url_for("PaymentConfirmFromUser"))
		else :
			user.status = "pending"	
			db.session.commit()
			flash("Status berhasil di perbaharui","success")
			return redirect(url_for("PaymentConfirmFromUser"))			
	return render_template("admin/edit_confirm.html",form=form)	



############# user ############################


@app.route("/register",methods=["GET","POST"])
def UserRegister():
	form = SuperuserRegisterForm()
	if form.validate_on_submit():
		trial = datetime.today()
		start = trial + timedelta(days=7)
		renew = start + timedelta(days=365)
		hass = generate_password_hash(form.password.data,method="sha256")
		user = User(username=form.username.data,email=form.email.data,phone=form.phone.data,company=form.company.data,password=hass,trial_date=trial,start_date=start,renew_date=renew,role="user",status="trial")
		check_email = User.query.filter_by(email=form.email.data).all()
		if len(check_email) > 0 :
			flash("Email telah terdaftar","danger")
		else :	
			db.session.add(user)
			db.session.commit()
			log = User.query.filter_by(email=form.email.data).first()
			login_user(log)
			flash("Anda berhasil mendaftar","success")
			return redirect(url_for("UserDashboard"))
	return render_template("user/register.html",form=form)	



@app.route("/login",methods=["GET","POST"])
def UserLogin():
	form = UserLoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user :
			if user.role == "SuperUser":
				return render_template("user/login.html",form=form)
			else :	
				if check_password_hash(user.password,form.password.data):
					login_user(user)
					flash("Anda berhasil masuk","success")
					return redirect(url_for("UserDashboard"))
		flash("Email atau Password salah","danger")
	return render_template("user/login.html",form=form)


@app.route("/logout",methods=["GET","POST"])
@login_required
def Logout():
	logout_user()	
	return redirect(url_for("Index")) 		



@app.route("/forgot-password",methods=["GET","POST"])
def ForgotPassword():
	form = ForgotPasswordForm()
	if form.validate_on_submit():
		email = form.email.data
		user = User.query.filter_by(email=email).first()
		if user :
			token = s.dumps(email, salt="email-confirm")

			msg = Message("Reset Password", sender="easyhrd.com@gmail.com", recipients=[email])

			link = url_for("ResetPassword", token=token, _external=True)

			msg.body = "your link is {}".format(link)
			mail.send(msg)
		
			flash("cek inbox email anda","success")
			return redirect(url_for("UserLogin"))
		else :
			flash("Invalid email","danger")
			return render_template("user/forgot_password.html",form=form)
	return render_template("user/forgot_password.html",form=form)


@app.route("/reset-password/<token>",methods=["GET","POST"])
def ResetPassword(token):
	form = ResetPasswordForm()
	try :
		email = s.loads(token, salt="email-confirm", max_age=3000)
		if form.validate_on_submit():
			user = User.query.filter_by(email=email).first()
			hass_pass = generate_password_hash(form.password.data,method="sha256")
			user.password = hass_pass
			db.session.commit()

			flash("Password berhasil di rubah,silakan login","success")
			return redirect(url_for("UserLogin"))
	except :
		flash("Link Expired","danger")
		return redirect(url_for("ForgotPassword"))

	return render_template("user/reset_password.html",form=form)	



@app.route("/dashboard/reset-password",methods=["GET","POST"])
@login_required
def UserResetPassword():
	user = User.query.filter_by(id=current_user.id).first()
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hass_pass = generate_password_hash(form.password.data,method="sha256")
		user.password = hass_pass
		db.session.commit()
		flash("Password berhasil di rubah","success")
		return redirect(url_for("UserDashboard"))
	return render_template("user/user_reset_password.html",form=form)	




######################### dashboard ##############



@app.route("/dashboard",methods=["GET","POST"])
@login_required
def UserDashboard():
	if current_user.role == "user":
		employe = len(Employe.query.filter_by(owner_id=current_user.id).all())
		cuti = len(Attendance.query.filter_by(attener_owner=current_user.id,status="Belum Di Setujui").all())
		return render_template("user/dashboard.html",employe=employe,cuti=cuti)
	else :			
		employe = len(Employe.query.filter_by(owner_id=current_user.users).all())
		cuti = len(Attendance.query.filter_by(attener_owner=current_user.users,status="Belum Di Setujui").all())
		return render_template("user/dashboard.html",employe=employe,cuti=cuti)		




######################## User Account #####################
@app.route("/dashboard/edit-account",methods=["GET","POST"])
@login_required
def UserEditAccount():
	user = current_user
	form = UserEditAccountForm()
	form.username.data = user.username
	form.company.data = user.company
	form.phone.data = user.phone
	form.email.data = user.email
	if form.validate_on_submit():
		useremail = request.form["email"]
		check_email = User.query.filter_by(email=useremail).all()
		if len(check_email) > 0 :
			if user.email == useremail :	
				user.username = request.form["username"]
				user.company = request.form["company"]
				user.phone = request.form["phone"]
				user.email = useremail
				db.session.commit()
				flash("Profile berhasil di perbaharui","success")
				return redirect(url_for("UserDashboard"))
			else :	
				flash("Email telah terdaftar,silakan pakai email lain","danger")		
		else :	  
			user.username = request.form["username"]
			user.company = request.form["company"]
			user.phone = request.form["phone"]
			user.email = useremail
			db.session.commit()
			flash("Profile berhasil di perbaharui","success")
			return redirect(url_for("UserDashboard"))
	return render_template("user/edit_account.html",form=form)	








################ Admin Route ############################### 
@app.route("/dashboard/admin",methods=["GET","POST"])
@login_required
@roles_required(role="user")
def AllAdmin():
	admins = User.query.filter_by(users=current_user.id).all()
	return render_template("user/all_admin.html",admins=admins)



@app.route("/dashboard/add-admin",methods=["GET","POST"])
@login_required
@roles_required(role="user")
def AddAdmin():
	form = UserRegisterForm()
	if form.validate_on_submit():
		hass = generate_password_hash(form.password.data,method="sha256")	
		user = User(username=form.username.data,email=form.email.data,password=hass,role="admin",users=current_user.id)
		check_email = User.query.filter_by(email=form.email.data).all()
		if len(check_email) > 0 :
			flash("Email telah terdaftar","danger")
		else :
			db.session.add(user)
			db.session.commit()	
			flash("Admin berhasil di tambah","success")
			return redirect(url_for("AllAdmin"))
	return render_template("user/add_admin.html",form=form)	


@app.route("/dashboard/delete-admin/<string:id>",methods=["GET","POST"])
@login_required
@roles_required(role="user")
def DeleteAdmin(id):	
	admin = User.query.filter_by(id=id).first()
	if current_user.id == admin.users :
		db.session.delete(admin)
		db.session.commit()
		flash("Admin berhasil di hapus","success")
		return redirect(url_for("AllAdmin"))
	else :
		return "no access"



############################## Employe Route ###################################
@app.route("/dashboard/add-employe",methods=["GET","POST"])
@login_required
def AddEmploye():
	form = AddEmployeForm()
	if form.validate_on_submit():
		if current_user.role == "user":				
			employe = Employe(name=form.name.data,nik=form.nik.data,email=form.email.data,phone=form.phone.data,departement=form.departement.data,salary=form.salary.data,added=form.added.data,cabang=form.cabang.data,education=form.education.data,institut=form.institut.data,jurusan=form.jurusan.data,birth=form.birth.data,address=form.address.data,gender=form.gender.data,status=form.status.data,religion=form.religion.data,ktp=form.ktp.data,npwp=form.npwp.data,bank=form.bank.data,bank_account=form.bank_account.data,no_rek=form.no_rek.data,bpjs_ketenagakerjaan=form.bpjs_ketenagakerjaan.data,bpjs_kesehatan=form.bpjs_kesehatan.data,notes=form.notes.data,owner_id=current_user.id,image_name="avatar.png")	
			db.session.add(employe)
			db.session.commit()
			flash("Data pegawai berhasil di tambah","success")
			return redirect(url_for("AllEmploye"))
		else :
			employe = Employe(name=form.name.data,nik=form.nik.data,email=form.email.data,phone=form.phone.data,departement=form.departement.data,salary=form.salary.data,added=form.added.data,cabang=form.cabang.data,education=form.education.data,institut=form.institut.data,jurusan=form.jurusan.data,birth=form.birth.data,address=form.address.data,gender=form.gender.data,status=form.status.data,religion=form.religion.data,ktp=form.ktp.data,npwp=form.npwp.data,bank=form.bank.data,bank_account=form.bank_account.data,no_rek=form.no_rek.data,bpjs_ketenagakerjaan=form.bpjs_ketenagakerjaan.data,bpjs_kesehatan=form.bpjs_kesehatan.data,notes=form.notes.data,owner_id=current_user.users,image_name="avatar.png")
			db.session.add(employe)
			db.session.commit()
			flash("Data pegawai berhasil di tambah","success")
			return redirect(url_for("AllEmploye"))

	return render_template("user/add_employe.html",form=form)	


@app.route("/dashboard/employe",methods=["GET","POST"])
@login_required
def AllEmploye():
	if current_user.role == "user":
		employer = Employe.query.filter_by(owner_id=current_user.id).all()
		length = len(employer)		
		form = SearchForm()
		if form.validate_on_submit():
			employer = Employe.query.filter_by(name=form.search.data,owner_id=current_user.id).all()
			len_search = len(employer)
			if len_search == 0 :
				flash("Maaf tidak ada pegawai yang ditemukan. Harap di cek kembali penulisan yang benar","danger")
				return redirect(url_for("AllEmploye"))
			else :	
				return render_template("user/all_employe.html",employer=employer,length=length,form=form)
		return render_template("user/all_employe.html",employer=employer,length=length,form=form)
	else :
		employer = Employe.query.filter_by(owner_id=current_user.users).all()
		length = len(employer)		
		form = SearchForm()
		if form.validate_on_submit():
			employer = Employe.query.filter_by(name=form.search.data,owner_id=current_user.users).all()
			len_search = len(employer)			
			if len_search == 0 :
				flash("Maaf tidak ada pegawai yang ditemukan. Harap di cek kembali penulisan yang benar","danger")
				return redirect(url_for("AllEmploye"))
			else :	
				return render_template("user/all_employe.html",employer=employer,length=length,form=form)
		return render_template("user/all_employe.html",employer=employer,length=length,form=form)


@app.route("/dashboard/employe/<string:id>",methods=["GET","POST"])
@login_required
def EmployeId(id):
	employe = Employe.query.filter_by(id=id).first()
	if current_user.id == employe.owner_id or current_user.users == employe.owner_id: 
		return render_template("user/employe.html",employe=employe)		
	else :
		return "No access"
	


@app.route("/dashboard/delete-employe/<string:id>",methods=["GET","POST"])
@login_required
def DeleteEmploye(id):
	employe = Employe.query.filter_by(id=id).first()
	if current_user.id == employe.owner_id or current_user.users == employe.owner_id :
		db.session.delete(employe)
		db.session.commit()
		flash("Pegawai berhasil di hapus","success")
		return redirect(url_for("AllEmploye"))
	else :
		return "no access"	




@app.route("/dashboard/edit-employe/<string:id>",methods=["GET","POST"])
@login_required
def EditEmploye(id):
	employe = Employe.query.filter_by(id=id).first()
	form = AddEmployeForm()
	if current_user.id == employe.owner_id or current_user.users == employe.owner_id :
		form.name.data = employe.name
		form.nik.data = employe.nik
		form.email.data = employe.email
		form.phone.data = employe.phone
		form.departement.data = employe.departement		
		form.salary.data = employe.salary
		form.added.data = employe.added
		form.cabang.data = employe.cabang
		form.education.data = employe.education
		form.institut.data = employe.institut
		form.jurusan.data = employe.jurusan
		form.ktp.data = employe.ktp 
		form.npwp.data = employe.npwp
		form.bank.data = employe.bank
		form.bank_account.data = employe.bank_account
		form.no_rek.data = employe.no_rek
		form.bpjs_kesehatan.data = employe.bpjs_kesehatan
		form.bpjs_ketenagakerjaan.data = employe.bpjs_ketenagakerjaan
		form.birth.data = employe.birth
		form.address.data = employe.address
		form.gender.data = employe.gender
		form.status.data = employe.status
		form.religion.data = employe.religion
		form.notes.data = employe.notes
		if form.validate_on_submit():
			birthday = datetime.strptime(request.form["birth"], '%m/%d/%Y').strftime('%Y-%m-%d')	
			add = datetime.strptime(request.form["added"], '%m/%d/%Y').strftime('%Y-%m-%d')
			employe.name = request.form["name"]
			employe.email = request.form["email"]
			employe.phone = request.form["phone"]
			employe.departement = request.form["departement"]			
			employe.salary = request.form["salary"]
			employe.added = add
			employe.birth = birthday
			employe.address = request.form["address"]
			employe.gender = request.form["gender"]
			employe.status = request.form["status"]
			employe.religion = request.form["religion"]
			employe.notes = request.form["notes"]
			employe.nik = request.form["nik"]
			employe.cabang = request.form["cabang"]
			employe.education = request.form["education"]
			employe.institut = request.form["institut"]
			employe.jurusan = request.form["jurusan"]
			employe.ktp = request.form["ktp"]
			employe.npwp = request.form["npwp"]
			employe.bank = request.form["bank"]
			employe.bank_account = request.form["bank_account"]
			employe.no_rek = request.form["no_rek"]
			employe.bpjs_kesehatan = request.form["bpjs_kesehatan"]
			employe.bpjs_ketenagakerjaan = request.form["bpjs_ketenagakerjaan"]


			db.session.commit()
			flash("Data berhasil di edit","success")
			return redirect(url_for("AllEmploye"))
	else :
		return "No access"

	return render_template("user/edit_employe.html",form=form)	



@app.route("/dashboard/edit-photo/<string:id>",methods=["GET","POST"])
@login_required
def EditPhoto(id):
	form = EditPhotoForm()
	employe = Employe.query.filter_by(id=id).first()
	if form.validate_on_submit():
		filename = images.save(form.image.data)
		employe.image_name = filename
		db.session.commit()
		flash("Photo berhasil di rubah","success")
		return redirect(url_for("AllEmploye"))
	return render_template("user/edit_photo.html",form=form)	
	
	
	
	
	
##################### invoice #################
@app.route("/dashboard/invoice",methods=["GET","POST"])
@login_required
def UserInvoice():
	user = User.query.filter_by(id=current_user.id).first()
	return render_template("user/invoice.html",user=user)	


@app.route("/dashboard/renew/invoice",methods=["GET","POST"])
@login_required
def RenewInvoice():
	user = User.query.filter_by(id=current_user.id).first()
	tempo = user.renew_date + timedelta(days=30)
	return render_template("user/renew_invoice.html",user=user,tempo=tempo)	



@app.route("/dashboard/konfirmasi",methods=["GET","POST"])
@login_required
def PaymentConfirm():
	form = ConfirmPaymentForm()
	if form.validate_on_submit():
		today = datetime.today()
		pay = Confirm(username=current_user.username,email=current_user.email,from_bank=form.from_bank.data,to_bank=form.to_bank.data,bank_account=form.bank_account.data,date=today,status="pending")
		db.session.add(pay)
		db.session.commit()
		flash("Terima Kasih,Konfirmasi anda telah kami terima","success")
		return redirect(url_for("UserDashboard"))
	return render_template("user/konfirmasi.html",form=form)








################################### Blog ############################################################
# front page blog
@app.route("/blog",methods=["GET","POST"])
def AllBlog():
	blogs = Blog.query.all()
	return render_template("blog/front_page.html",blogs=blogs)


@app.route("/add-blog",methods=["GET","POST"])
@login_required
@roles_required(role="SuperUser")
def AddBlog():
	form = AddBlogPostForm()
	if form.validate_on_submit():
		today = datetime.today()
		filename = images.save(form.image.data)
		blog = Blog(title=form.title.data,body=form.body.data,slug=form.slug.data,date=today,image=filename)
		db.session.add(blog)
		db.session.commit()
		flash("bloger","success")
		return redirect(url_for("AllBlog"))
	return render_template("blog/add_blog.html",form=form)

@app.route("/blog/<slug>",methods=["GET","POST"])
def Post(slug):
	blog = Blog.query.filter_by(slug=slug).first()
	return render_template("blog/post.html",blog=blog)

		


################################ KPI ##########################################
@app.route("/dashboard/kpi/employe",methods=["GET","POST"])
@login_required
def AllEmployeKpi():	
	if current_user.role == "user":
		employer = Employe.query.filter_by(owner_id=current_user.id).all()
		length = len(employer)		
		form = SearchForm()
		if form.validate_on_submit():
			employer = Employe.query.filter_by(name=form.search.data,owner_id=current_user.id).all()
			len_search = len(employer)
			if len_search == 0 :
				flash("Maaf tidak ada pegawai yang ditemukan. Harap di cek kembali penulisan yang benar","danger")
				return redirect(url_for("AllEmployeKpi"))
			else :	
				return render_template("kpi/all_employe.html",employer=employer,length=length,form=form)
		return render_template("kpi/all_employe.html",employer=employer,length=length,form=form)
	else :
		employer = Employe.query.filter_by(owner_id=current_user.users).all()
		length = len(employer)		
		form = SearchForm()
		if form.validate_on_submit():
			employer = Employe.query.filter_by(name=form.search.data,owner_id=current_user.users).all()
			len_search = len(employer)			
			if len_search == 0 :
				flash("Maaf tidak ada pegawai yang ditemukan. Harap di cek kembali penulisan yang benar","danger")
				return redirect(url_for("AllEmployeKpi"))
			else :	
				return render_template("kpi/all_employe.html",employer=employer,length=length,form=form)
		return render_template("kpi/all_employe.html",employer=employer,length=length,form=form)



@app.route("/dashboard/kpi/employe/<string:id>",methods=["GET","POST"])
@login_required
def KpiPerEmploye(id):
	employe = Employe.query.filter_by(id=id).first()
	form = AddKpiForm()
	kpis = Kpi.query.filter_by(kpis_id=employe.id).order_by(Kpi.date.desc()).all()
	if form.validate_on_submit():
		today = datetime.today()
		target =form.target.data 
		complish = form.complish.data
		result = complish - target  
		final = result * 100.0 / target 
		if current_user.role == "user":
			kpi = Kpi(key=form.key.data,indicator=form.indicator.data,target=target,complish=complish,result=final,date=today,kpis_id=employe.id,kpier_id=current_user.id,kpier_owner=current_user.id)
			db.session.add(kpi)
			db.session.commit()
			flash("Input berhasil ditambah","success")
			return redirect(url_for("KpiPerEmploye",id=id))
		else :
			kpi = Kpi(key=form.key.data,indicator=form.indicator.data,target=target,complish=complish,result=final,date=today,kpis_id=employe.id,kpier_id=current_user.id,kpier_owner=current_user.users)
			db.session.add(kpi)
			db.session.commit()
			flash("Input berhasil di tambah","success")
			return redirect(url_for("KpiPerEmploye",id=id))
	return render_template("kpi/employe.html",form=form,employe=employe,kpis=kpis)



@app.route("/dashboard/kpi/employe/edit/<string:id>",methods=["GET","POST"])
@login_required
def EditKpi(id):
	kpi = Kpi.query.filter_by(id=id).first()
	employe = Employe.query.filter_by(id=kpi.kpis_id).first()
	kpis = Kpi.query.filter_by(kpis_id=employe.id).order_by(Kpi.date.desc()).all()
	id = employe.id 
	form = AddKpiForm()
	form.key.data = kpi.key 
	form.indicator.data = kpi.indicator
	form.target.data = kpi.target
	form.complish.data = kpi.complish
	if form.validate_on_submit():
		target = int(request.form["target"])
		complish = int(request.form["complish"])
		result = complish - target 
		final = result * 100.0 / target
		kpi.key = request.form["key"]
		kpi.indicator = request.form["indicator"]
		kpi.target = target
		kpi.complish = complish 
		kpi.result = final 
		db.session.commit() 
		flash("kpi berhasil di edit","success")
		return redirect(url_for("KpiPerEmploye",id=id))
	return render_template("kpi/employe.html",form=form,employe=employe,kpis=kpis)	




#################################### Attendance route ########################################
@app.route("/dashboard/attendance/employe/<string:id>",methods=["GET","POST"])
@login_required
def EmployeAttendance(id):
	employe = Employe.query.filter_by(id=id).first()
	form = AddAttendanceForm()
	attendances = Attendance.query.filter_by(attens_id=employe.id).order_by(Attendance.id.desc()).all()
	if form.validate_on_submit():
		start = form.start.data 
		end = form.end.data 
		today = datetime.today()
		if current_user.role == "user":
			cuti = Attendance(name=employe.name,departement=employe.departement,start=start,end=end,reason=form.reason.data,status=form.status.data,attens_id=employe.id,attener_id=current_user.id,attener_owner=current_user.id,date=today)
			db.session.add(cuti)
			db.session.commit()
			flash("Data Cuti Berhasil Di Tambah","success")
			return redirect(url_for("EmployeAttendance",id=id))
		else :
			cuti = Attendance(name=employe.name,departement=employe.departement,start=start,end=end,reason=form.reason.data,status=form.status.data,attens_id=employe.id,attener_id=current_user.id,attener_owner=current_user.users,date=today)
			db.session.add(cuti)
			db.session.commit()
			flash("Data Cuti Berhasil Di Tambah","success")
			return redirect(url_for("EmployeAttendance",id=id))
	return render_template("cuti/employe.html",attendances=attendances,form=form,employe=employe)		


@app.route("/dashboard/attendance/employe/edit/<string:id>",methods=["GET","POST"])
@login_required
def EditEmployeAttenance(id):
	attendance = Attendance.query.filter_by(id=id).first()
	employe = Employe.query.filter_by(id=attendance.attens_id).first()
	attendances = Attendance.query.filter_by(attens_id=employe.id).order_by(Attendance.id.desc()).all()
	id = employe.id 
	form = AddAttendanceForm()
	form.start.data = attendance.start
	form.end.data = attendance.end 
	form.reason.data = attendance.reason
	form.status.data = attendance.status
	if form.validate_on_submit():
		start =  datetime.strptime(request.form["start"], '%m/%d/%Y').strftime('%Y-%m-%d')	
		end =datetime.strptime(request.form["end"], '%m/%d/%Y').strftime('%Y-%m-%d')	
		attendance.start = start
		attendance.end = end
		attendance.status = request.form["status"]
		attendance.reason = request.form["reason"]
		db.session.commit()
		flash("Status Berhasil Di Rubah","success")
		return redirect(url_for("EmployeAttendance",id=id))
	return render_template("cuti/employe.html",attendances=attendances,form=form,employe=employe)



@app.route("/dashboard/attendance/list",methods=["GET","POST"])
@login_required
def AttendanceList():
	if current_user.role == "user":
		attendances = Attendance.query.filter_by(attener_owner=current_user.id,status="Belum Di Setujui").all() 
		return render_template("cuti/cuti_list.html",attendances=attendances)
	else :
		attendances = Attendance.query.filter_by(attener_owner=current_user.users,status="Belum Di Setujui").all() 
		return render_template("cuti/cuti_list.html",attendances=attendances)



######################### Submit Delete ###############################
@app.route("/dashboard/confirm/delete/<string:status>/<string:id>",methods=["GET","POST"])
@login_required
def ConfirmDelete(status,id):
	if status == "cuti":
		form = SubmitForm()
		atten = Attendance.query.filter_by(id=id).first()
		employe = Employe.query.filter_by(id=atten.attens_id).first()
		id = employe.id
		if form.validate_on_submit():		
			db.session.delete(atten)
			db.session.commit()
			flash("Data Cuti Berhasil Di Hapus","success")
			return redirect(url_for("EmployeAttendance",id=id))
		return render_template("user/confirm_delete.html",form=form,status=status,employe=employe)		
	elif status == "performa":
		form = SubmitForm()
		kpi = Kpi.query.filter_by(id=id).first()
		employe = Employe.query.filter_by(id=kpi.kpis_id).first()
		id = employe.id
		if form.validate_on_submit():		
			db.session.delete(kpi)
			db.session.commit()
			flash("Data Kpi Berhasil Di Hapus","success")
			return redirect(url_for("KpiPerEmploye",id=id))
		return render_template("user/confirm_delete.html",form=form,status=status,employe=employe)	
	else :
		return "Dear God,Punch This Little Fucker"
		
		






		







if __name__ == "__main__":
	#manager.run()
	app.run(host='0.0.0.0')
