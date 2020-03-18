#coding=utf-8
import os
from datetime import datetime
from flask import Flask, render_template, session, redirect, \
				  url_for, flash, current_app, request
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, LoginManager, login_required, \
						login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, \
					BooleanField, IntegerField, ValidationError
from wtforms.validators import Required, Length, Regexp
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


'''
Config
'''
basedir = os.path.abspath(os.path.dirname(__file__))

def make_shell_context():
	return dict(app=app, db=db, Device=Device, Role=Role)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['AdminPassword'] = 666666
app.config['SECRET_KEY'] = "this is a secret_key"
db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_shell_context))
login_manager = LoginManager(app)

login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = u"你需要登录才能访问这个页面."


'''
Models
'''
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, unique=True)
	name = db.Column(db.String(64), primary_key=True)
	users = db.relationship('Device', backref='role', lazy='dynamic')
	password = db.Column(db.String(128), default=123456)

	@staticmethod
	def insert_roles():
		roles = ('Student','Admin')
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			db.session.add(role)
		db.session.commit()


	def __repr__(self):
		return '<Role %r>' %self.name

	#初次运行程序时生成初始管理员的静态方法
	@staticmethod
	def generate_admin():
		admin = Role.query.filter_by(name='Admin').first()
		# u = Device.query.filter_by(role=admin).first()
		if admin is None:
			admin = Device(id = 000000, name ='Admin', password = current_app.config['AdminPassword'])
			#role = Role.query.filter_by(name='Admin').first()) # TODO
			db.session.add(admin)
		db.session.commit()

	def verify_password(self, password):
		return self.time == password


class Device(UserMixin, db.Model):
	__tablename__ = 'devices'
	id = db.Column(db.Integer, primary_key=True)
	lab = db.Column(db.String(64), unique=True, index=True)
	name = db.Column(db.String(64), index=True)
	time = db.Column(db.DateTime, default=datetime.utcnow)
	role_name = db.Column(db.String(64), db.ForeignKey('roles.name'))

	def __init__(self, **kwargs):
		super(Device, self).__init__(**kwargs)
		#新添加的实验设备，初始其购置人为学生。
		if self.role is None:
			self.role = Role.query.filter_by(name='Student').first()

	def __repr__(self):
		return '<Device %r>' %self.name


'''
Forms
'''
class LoginForm(FlaskForm):
	id = StringField(u'账号', validators=[Required()])
	password = PasswordField(u'密码', validators=[Required()])
	remember_me = BooleanField(u'记住我')
	submit = SubmitField(u'登录')


class SearchForm(FlaskForm):
	id = IntegerField(u'设备号', validators=[Required(message=u'请输入数字')])
	submit = SubmitField(u'搜索')


class DeviceForm(FlaskForm):
	name = StringField(u'设备名', validators=[Required()])
	id = IntegerField(u'设备编号', validators=[Required(message=u'请输入数字')])
	submit = SubmitField(u'添加')

	def validate_number(self, field):
		if Device.query.filter_by(number=field.data).first():
			raise ValidationError(u'此设备已存在，请检查考号！')

'''
class EditForm(FlaskForm):
	username = StringField(u'姓名', validators=[Required()])
	number = IntegerField(u'考号', validators=[Required(message=u'请输入数字')])
	password = StringField(u'密码', validators=[Required(), Length(1,64),\
									Regexp('^[a-zA-Z0-9_.]*$', 0, \
											u'密码由字母、数字和_.组成')])
	role = SelectField(u'身份', coerce=int)
	submit = SubmitField(u'修改')

	def __init__(self, user, *args, **kargs):
		super(EditForm, self).__init__(*args, **kargs)
		self.role.choices = [(role.id, role.name)
							 for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_number(self, field):
		if field.data != self.user.number and \
				Device.query.filter_by(number=field.data).first():
			raise ValidationError(u'此学生已存在，请检查考号！')
'''

'''
views
'''
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
	form = SearchForm()
	admin = Role.query.filter_by(name='Admin').first()
	if form.validate_on_submit():
		#获得设备列表，其id包含form中的数字
		devices = Device.query.filter(Device.lab.like('%{}%'.format(form.id.data))).all()
	else:
		devices = Device.query.order_by(Device.role_name.desc(), Device.lab.asc()).all()
	return render_template('index.html', form=form, devices=devices, admin=admin)


#增加新设备
@app.route('/add-user', methods=['GET', 'POST'])
@login_required
def add_device():
	form = DeviceForm()
	if form.validate_on_submit():
		user = Device(name=form.name.data, id=form.id.data)
		db.session.add(user)
		flash(u'成功添加设备')
		return redirect(url_for('index'))
	return render_template('add_user.html', form=form)


#移除设备
@app.route('/remove-user/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_device(id):
	device = Device.query.get_or_404(id)
	if device.role == Role.query.filter_by(name='Admin').first():
		flash(u'不能删除管理员添加的设备')
	else:
		db.session.delete(device)
		flash(u'成功删除此设备')
	return redirect(url_for('index'))

'''
#修改考生资料
@app.route('/edit-user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
	user = Device.query.get_or_404(id)
	form = EditForm(user=user)
	if form.validate_on_submit():
		user.username = form.username.data
		user.number = form.number.data
		user.password = form.password.data
		user.role = Role.query.get(form.role.data)
		db.session.add(user)
		flash(u'个人信息已更改')
		return redirect(url_for('index'))
	form.username.data = user.username
	form.number.data = user.number
	form.password.data = user.password
	form.role.data = user.role_id
	return render_template('edit_user.html', form=form, user=user)
'''

#登录，系统只允许管理员登录
@app.route('/login', methods=['GET', 'POST'])
def login():
	form  = LoginForm()
	if form.validate_on_submit():
		user = Role.query.filter_by(number=form.id.data).first()
		if user is not None and user.verify_password(form.password.data):
			if user.role != Role.query.filter_by(name='Admin').first(): #TODO
				flash(u'系统只对管理员开放，请联系管理员获得权限！')
			else:
				login_user(user, form.remember_me.data)
				return redirect(url_for('index'))
		flash(u'用户名或密码错误！')
	return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash(u'成功注销！')
	return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

#加载用户的回调函数
@login_manager.user_loader
def load_user(user_name): #TODO
	return Role.query.get(int(user_name))

'''
增加命令'python app.py init' 
以增加身份与初始管理员帐号
'''
@manager.command
def init():
	from app import Role
	Role.insert_roles()
	Role.generate_admin()


if __name__=='__main__':
	manager.run()