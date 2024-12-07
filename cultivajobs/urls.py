from django.contrib import admin
from django.urls import path, include
from cultivajobsApp.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('sobrenosotros/', sobreNosotros, name='sobrenosotros'),
    path('registroestudiante/', registrarestudiante, name='registroestudiante'),
    path('registroempleador/', registrarempleador, name='registroempleador'),
    path('registro-exitoso/', registro_exitoso, name='registro_exitoso'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', custom_login, name='login'),  # Vista personalizada de login
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('menu/estudiante/', menu_estudiante, name='menu_estudiante'),
    path('menu/empleador/', menu_empleador, name='menu_empleador'),
    path('dashboard/', dashboard, name='dashboard'),
    path('menu/ofertas/', menu_ofertas, name='menu_ofertas'), 
    path('menu/verofertas/', ver_ofertas, name='ver_ofertas'),  
    path('postular/<int:oferta_id>/', postular_oferta, name='postular_oferta'),
    path('verificacion_email/', verificar_codigo, name='verificacion_email'),  # Nueva URL para verificación de email
    path('perfil_estudiante/', actualizar_perfil_estudiante, name='perfil_estudiante'),
    path('postulacion/<int:oferta_id>/', postular_oferta, name='postulacion'),
    path('cancelar_postulacion/<int:oferta_id>/', cancelar_postulacion, name='cancelar_postulacion'),
    path('buscar/', buscar_ofertas, name='buscar_ofertas'),
     path('vercandidatos/<int:oferta_id>/', ver_candidatos, name='vercandidatos'),


]
