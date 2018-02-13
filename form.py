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


class SuperuserRegisterForm(FlaskForm):
	username = StringField("Username",validators=[InputRequired(),Length(max=100)])
	email = StringField("Email",validators=[InputRequired(),Length(max=100),Email()])
	password = PasswordField("Password",validators=[InputRequired(),Length(min=6,max=100)])
	phone = StringField("Phone",validators=[Length(max=100),InputRequired()])
	company = StringField("Perusahaan",validators=[Length(max=100),InputRequired()])

class OwnerEditUserForm(FlaskForm):
	renew = DateField("Renew date",format="%m/%d/%Y")
	status = SelectField("Status",choices= [("trial","trial"),("pending","pending"),("active","active")])

class OwnerEditConfirmForm(FlaskForm):
	status = SelectField("Status",choices= [("pending","pending"),("paid","paid")])

class UserEditAccountForm(FlaskForm):
	username = StringField("Username",validators=[InputRequired(),Length(max=100)])
	email = StringField("Email",validators=[InputRequired(),Length(max=100),Email()])	
	phone = StringField("Phone",validators=[Length(max=100),InputRequired()])
	company = StringField("Perusahaan",validators=[Length(max=100),InputRequired()])


class UserLoginForm(FlaskForm):
	email = StringField("Email",validators=[InputRequired(),Length(max=100),Email()])
	password = PasswordField("Password",validators=[InputRequired(),Length(max=100)])

class ForgotPasswordForm(FlaskForm):
	email = StringField("Email",validators=[InputRequired(),Length(max=100),Email()])	

class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password",validators=[InputRequired(),Length(min=8)])	


class SearchForm(FlaskForm):
	search = StringField("Cari berdasarkan nama pegawai",validators=[InputRequired(),Length(max=200)])


'''
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
	notes = TextAreaField("Info Tambahan")

'''

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



class OwnerRegisterForm(FlaskForm):
	username = StringField("Username",validators=[InputRequired(),Length(max=100)])
	email = StringField("Email",validators=[InputRequired(),Length(max=100),Email()])
	password = PasswordField("Password",validators=[InputRequired(),Length(min=6,max=100)])
	double = PasswordField("Password Lage",validators=[InputRequired(),Length(min=6,max=100)])



class OwnerLoginForm(FlaskForm):
	username = StringField("Username",validators=[InputRequired(),Length(max=100)])	
	password = PasswordField("Password",validators=[InputRequired(),Length(min=6,max=100)])
	double = PasswordField("Password Lage",validators=[InputRequired(),Length(min=6,max=100)])
	


class ConfirmPaymentForm(FlaskForm):
	from_bank = StringField("Nama Bank",validators=[InputRequired(),Length(max=100)])
	bank_account = StringField("Nama Pemilik Rekening",validators=[InputRequired(),Length(max=100)])
	to_bank = SelectField("Bank Tujuan",choices= [("Mandiri ","Mandiri"),("BRI","BRI")])




class AddBlogPostForm(FlaskForm):
	title = StringField("Title",validators=[InputRequired(),Length(max=200)])
	slug = StringField("Slug",validators=[InputRequired(),Length(max=200)])
	body = TextAreaField("Body")
	image = FileField("Upload photo",validators=[FileAllowed(images,"Images Only")])




########## Employe Section #######################
'''class AddEmployeForm(FlaskForm):
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
	notes = TextAreaField("Info Tambahan")'''


class AddEmployeForm(FlaskForm):
	name = StringField("Nama",validators=[Length(max=100)])
	nik = StringField("NIK",validators=[Length(max=200)]) 
	email = StringField("Email",validators=[Length(max=100)])
	phone = StringField("Telepon",validators=[Length(max=100)])
	departement = StringField("Departement",validators=[Length(max=100)]) 	
	salary = StringField("Gaji",validators=[Length(max=100)])
	added = DateField("Mulai Bekerja",format="%m/%d/%Y")
	cabang = StringField("Penempatan Kerja",validators=[Length(max=100)])
	education = StringField("Pendidikan Terakhir",validators=[Length(max=100)])
	institut = StringField("Nama Institusi Pendidikan",validators=[Length(max=200)])
	jurusan = StringField("Jurusan / Program Studi",validators=[Length(max=200)])
	birth = DateField("Tanggal Lahir",format="%m/%d/%Y")
	address = TextAreaField("Alamat",validators=[Length(max=100)])
	gender = SelectField("Jenis Kelamin",choices= [("Laki Laki","Laki Laki"),("Perempuan","Perempuan")])
	status = SelectField("Status",choices= [("Menikah","Menikah"),("Belum Menikah","Belum Menikah")])
	religion = 	StringField("Agama",validators=[Length(max=100)])		
	ktp = StringField("Nomor KTP",validators=[Length(max=100)])	
	npwp = StringField("NPWP",validators=[Length(max=200)])
	bank = StringField("Nama Bank",validators=[Length(max=100)])
	bank_account = StringField("Nama Pemilik Rekening",validators=[Length(max=100)])
	no_rek = StringField("Nomor Rekening",validators=[Length(max=100)])
	bpjs_kesehatan = StringField("BPJS Kesehatan",validators=[Length(max=200)])
	bpjs_ketenagakerjaan = StringField("BPJS Ketenagakerjaan",validators=[Length(max=200)])
	notes = TextAreaField("Info Tambahan")

 










