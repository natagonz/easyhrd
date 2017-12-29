from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,TextAreaField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email, Length
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf.file import FileField, FileAllowed, FileRequired

images = UploadSet("images",IMAGES)


class UserRegisterForm(FlaskForm):
	username = StringField("Username",validators=[InputRequired(),Length(max=100)])
	email = StringField("Email",validators=[InputRequired(),Length(max=100),Email()])
	password = PasswordField("Password",validators=[InputRequired(),Length(min=6,max=100)])



class UserLoginForm(FlaskForm):
	email = StringField("Email",validators=[InputRequired(),Length(max=100),Email()])
	password = PasswordField("Password",validators=[InputRequired(),Length(max=100)])

class ForgotPasswordForm(FlaskForm):
	email = StringField("Email",validators=[InputRequired(),Length(max=100),Email()])	

class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password",validators=[InputRequired(),Length(min=8)])	



class AddEmployeForm(FlaskForm):
	name = StringField("Nama",validators=[Length(max=100)])
	email = StringField("Email",validators=[Length(max=100)])
	phone = StringField("Telepon",validators=[Length(max=100)])
	departement = StringField("Departement",validators=[Length(max=100)]) 
	skill = StringField("Skill",validators=[Length(max=100)])
	salary = StringField("Gaji",validators=[Length(max=100)])
	added = DateField("Mulai Bekerja",format="%m/%d/%Y")
	birth = DateField("Tanggal Lahir",format="%m/%d/%Y")
	address = StringField("Alamat",validators=[Length(max=100)])
	gender = SelectField("Jenis Kelamin",choices= [("Laki Laki","Laki Laki"),("Perempuan","Perempuan")])
	status = SelectField("Status",choices= [("Menikah","Menikah"),("Belum Menikah","Belum Menikah")])
	religion = 	StringField("Agama",validators=[Length(max=100)])
	image = FileField("Upload photo",validators=[FileAllowed(images,"Images Only")])


class AddReviewForm(FlaskForm):
	review = TextAreaField("Tulis Review")

class EditPhotoForm(FlaskForm):
	image = FileField("Upload photo",validators=[FileAllowed(images,"Images Only")])




class DeleteAdminForm(FlaskForm):
	submit = SubmitField("Delete")



class AddAttendanceForm(FlaskForm):
	name = StringField("Nama",validators=[Length(max=100)])
	departement = StringField("Departement",validators=[Length(max=100)]) 
	start = DateField("Dari Tanggal ",format="%m/%d/%Y")
	end = DateField("Sampai Tanggal",format="%m/%d/%Y")
	reason = StringField("Alasan Cuti")
	status = SelectField("Status",choices= [("Belum Di Setujui","Belum Di Setujui"),("Di Setujui","Di Setujui")])














