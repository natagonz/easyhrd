from flask import Flask , render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from form import UserRegisterForm ,UserLoginForm, AddEmployeForm, AddAttendanceForm,AddReviewForm,EditPhotoForm,ForgotPasswordForm,ResetPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_login import LoginManager , UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_uploads import UploadSet, IMAGES, configure_uploads





app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/hrd"
app.config["SECRET_KEY"] = "ini rahasia"
db = SQLAlchemy(app)
app.debug = True



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
	password = db.Column(db.String(100))
	role = db.Column(db.String(100))
	trial_date = db.Column(db.DateTime())
	start_date = db.Column(db.DateTime())
	renew_date = db.Column(db.DateTime())
	status = db.Column(db.String(100))
	users = db.Column(db.Integer())
	owner = db.relationship("Employe",backref="owner",lazy="dynamic")
	atten = db.relationship("Attendance",backref="atten",lazy="dynamic")
	reviewer = db.relationship("Review",backref="reviewer",lazy="dynamic")


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
	skill = db.Column(db.String(200))
	salary = db.Column(db.String(100))
	added = db.Column(db.DateTime())	
	birth = db.Column(db.DateTime())
	address = db.Column(db.String(100))
	gender = db.Column(db.String(100))
	status = db.Column(db.String(100))
	religion = db.Column(db.String(100))
	owner_id = db.Column(db.Integer(),db.ForeignKey("user.id"))
	image_name = db.Column(db.String(200))
	reviews = db.relationship("Review",backref="reviews",lazy="dynamic")





class Attendance(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	departement = db.Column(db.String(100))
	start = db.Column(db.DateTime())
	end = db.Column(db.DateTime())
	reason = db.Column(db.UnicodeText())
	status = db.Column(db.String(100))
	atten_id = db.Column(db.Integer(),db.ForeignKey("user.id"))



class Review(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	review = db.Column(db.UnicodeText())
	date = db.Column(db.DateTime())
	posted = db.Column(db.String(100))	
	reviews_id = db.Column(db.Integer(),db.ForeignKey("employe.id"))
	reviewer_id = db.Column(db.Integer(),db.ForeignKey("user.id"))
	reviewer_owner = db.Column(db.Integer())






#user loader
@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))




@app.route("/")
def Index():
	return render_template("index.html")



@app.route("/register",methods=["GET","POST"])
def UserRegister():
	form = UserRegisterForm()
	if form.validate_on_submit():
		trial = datetime.today()
		start = trial + timedelta(days=7)
		renew = start + timedelta(days=365)
		hass = generate_password_hash(form.password.data,method="sha256")
		user = User(username=form.username.data,email=form.email.data,password=hass,trial_date=trial,start_date=start,renew_date=renew,role="user",status="trial")
		check_email = User.query.filter_by(email=form.email.data).all()
		if len(check_email) > 0 :
			flash("Email telah terdaftar","danger")
		else :	
			db.session.add(user)
			db.session.commit()
			flash("Anda berhasil mendaftar","success")
			return redirect(url_for("UserLogin"))
	return render_template("user/register.html",form=form)	



@app.route("/login",methods=["GET","POST"])
def UserLogin():
	form = UserLoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user :
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
def UserDashboard():
	if current_user.role == "user":
		employe = len(Employe.query.filter_by(owner_id=current_user.id).all())
		cuti = len(Attendance.query.filter_by(atten_id=current_user.id).all())
		return render_template("user/dashboard.html",employe=employe,cuti=cuti)
	else :			
		employe = len(Employe.query.filter_by(owner_id=current_user.users).all())
		cuti = len(Attendance.query.filter_by(atten_id=current_user.users).all())
		return render_template("user/dashboard.html",employe=employe,cuti=cuti)		



################ Admin Route ############################### 
@app.route("/dashboard/admin",methods=["GET","POST"])
@login_required
def AllAdmin():
	admins = User.query.filter_by(users=current_user.id).all()
	return render_template("user/all_admin.html",admins=admins)



@app.route("/dashboard/add-admin",methods=["GET","POST"])
@login_required
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
			filename = images.save(form.image.data)
			employe = Employe(name=form.name.data,email=form.email.data,phone=form.phone.data,departement=form.departement.data,skill=form.skill.data,salary=form.salary.data,added=form.added.data,birth=form.birth.data,address=form.address.data,gender=form.gender.data,status=form.status.data,religion=form.religion.data,owner_id=current_user.id,image_name=filename)	
			db.session.add(employe)
			db.session.commit()
			flash("Data pegawai berhasil di tambah","success")
			return redirect(url_for("AllEmploye"))
		else :
			employe = Employe(name=form.name.data,email=form.email.data,phone=form.phone.data,departement=form.departement.data,skill=form.skill.data,salary=form.salary.data,added=form.added.data,birth=form.birth.data,address=form.address.data,gender=form.gender.data,status=form.status.data,religion=form.religion.data,owner_id=current_user.users,image_name=filename)	
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
		return render_template("user/all_employe.html",employer=employer)
	else :
		employer = Employe.query.filter_by(owner_id=current_user.users).all()
		return render_template("user/all_employe.html",employer=employer)



@app.route("/dashboard/employe/<string:id>",methods=["GET","POST"])
@login_required
def EmployeId(id):
	employe = Employe.query.filter_by(id=id).first()
	reviews = Review.query.filter_by(reviews_id=id).all()
	if current_user.id == employe.owner_id or current_user.users == employe.owner_id:  
		form = AddReviewForm()
		if form.validate_on_submit():	
			today = datetime.today()	
			if current_user.role == "user" :
				review = Review(review=form.review.data,date=today,posted=current_user.username,reviews_id=employe.id,reviewer_id=current_user.id,reviewer_owner=current_user.id)
				db.session.add(review)
				db.session.commit()
				flash("Review anda berhasil di tambahkan","success")
				return redirect(url_for("AllEmploye"))	
			else :
				review = Review(review=form.review.data,date=today,posted=current_user.username,reviews_id=employe.id,reviewer_id=current_user.id,reviewer_owner=current_user.users)
				db.session.add(review)
				db.session.commit()
				flash("Review anda berhasil di tambahkan","success")
				return redirect(url_for("AllEmploye"))	
	else :
		return "No access"
	return render_template("user/employe.html",employe=employe,form=form,reviews=reviews)



@app.route("/dashboard/delete-review/<string:id>",methods=["GET","POST"])
@login_required
def EditReview(id):
	review = Review.query.filter_by(id=id).first()
	if current_user.id == review.reviewer_id or current_user.id == review.reviewer_owner :
		db.session.delete(review)
		db.session.commit()
		flash("Review berhasil di hapus","success")
		return redirect(url_for("AllEmploye"))
	else :
		return "no access"	




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
		form.email.data = employe.email
		form.phone.data = employe.phone
		form.departement.data = employe.departement
		form.skill.data = employe.skill
		form.salary.data = employe.salary
		form.added.data = employe.added
		form.birth.data = employe.birth
		form.address.data = employe.address
		form.gender.data = employe.gender
		form.status.data = employe.status
		form.religion.data = employe.religion
		if form.validate_on_submit():
			birthday = datetime.strptime(request.form["birth"], '%m/%d/%Y').strftime('%Y-%m-%d')	
			add = datetime.strptime(request.form["added"], '%m/%d/%Y').strftime('%Y-%m-%d')
			employe.name = request.form["name"]
			employe.email = request.form["email"]
			employe.phone = request.form["phone"]
			employe.departement = request.form["departement"]
			employe.skill = request.form["skill"]
			employe.salary = request.form["salary"]
			employe.added = add
			employe.birth = birthday
			employe.address = request.form["address"]
			employe.gender = request.form["gender"]
			employe.status = request.form["status"]
			employe.religion = request.form["religion"]
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








#################################### Attendance route ########################################
@app.route("/dashboard/add-attendance",methods=["GET","POST"])
@login_required
def AddAttendance():
	form = AddAttendanceForm()
	user = User.query.filter_by(id=current_user.id).first()
	if form.validate_on_submit():
		if current_user.role == "user" :
			atten = Attendance(name=form.name.data,departement=form.departement.data,start=form.start.data,end=form.end.data,reason=form.reason.data,status=form.status.data,atten_id=current_user.id)
			db.session.add(atten)
			db.session.commit()
			flash("Data cuti berhasil di tambah","success")
			return redirect(url_for("UserDashboard"))
		else :
			atten = Attendance(name=form.name.data,departement=form.departement.data,start=form.start.data,end=form.end.data,reason=form.reason.data,status=form.status.data,atten_id=current_user.users)
			db.session.add(atten)
			db.session.commit()
			flash("Data cuti berhasil di tambah","success")
			return redirect(url_for("AllAttendance"))
				
	return render_template("user/add_attendance.html",form=form)	




@app.route("/dashboard/attendance",methods=["GET","POST"])
@login_required
def AllAttendance():
	if current_user.role == "user" :
		attendances = Attendance.query.filter_by(atten_id=current_user.id).all()
		return render_template("user/all_attendance.html",attendances=attendances)
	else :
		attendances = Attendance.query.filter_by(atten_id=current_user.users).all()
		return render_template("user/all_attendance.html",attendances=attendances)



@app.route("/dashboard/delete-attendance/<string:id>",methods=["GET","POST"])
@login_required
def DeleteAttendance(id):
	attendance = Attendance.query.filter_by(id=id).first()
	if current_user.id == attendance.atten_id or current_user.users == attendance.atten_id :
		db.session.delete(attendance)
		db.session.commit()
		flash("Data berhasil dihapus","success")
		return redirect(url_for("AllAttendance"))
	else :
		return "No access"




@app.route("/dashboard/edit-attendance/<string:id>",methods=["GET","POST"])
@login_required
def EdiAttendance(id):
	attendance = Attendance.query.filter_by(id=id).first()
	form = AddAttendanceForm()
	if current_user.id == attendance.atten_id or current_user.users == attendance.atten_id :
		form.name.data = attendance.name
		form.departement.data = attendance.departement
		form.start.data = attendance.start
		form.end.data = attendance.end 
		form.reason.data = attendance.reason
		form.status.data = attendance.status
		if form.validate_on_submit():
			start = datetime.strptime(request.form["start"], '%m/%d/%Y').strftime('%Y-%m-%d')	
			end = datetime.strptime(request.form["end"], '%m/%d/%Y').strftime('%Y-%m-%d')	
			attendance.name = request.form["name"]
			attendance.departement = request.form["departement"]
			attendance.start = start 
			attendance.end = end 
			attendance.reason = request.form["reason"]
			attendance.status = request.form["status"]
			db.session.commit()
			flash("Data berhasil di edit","success")
			return redirect(url_for("AllAttendance"))
	else :
		return "No access"		
	return render_template("user/edit_attendance.html",form=form)				

			

		
				
	
	
	
	
##################### invoice #################
@app.route("/dashboard/invoice",methods=["GET","POST"])
@login_required
def UserInvoice():
	user = User.query.filter_by(id=current_user.id).first()
	return render_template("user/invoice.html",user=user)	




@app.route("/dashboard/konfirmasi",methods=["GET","POST"])
@login_required
def PaymentConfirm():
	return render_template("user/konfirmasi.html")







if __name__ == "__main__":
	app.run()