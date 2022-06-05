from cProfile import run
from tasks.CompleteForm import CompleteForm
from classes.Errors import errors, process
from tasks.SendEmail import SendEmail

if __name__ == '__main__':
    try:
        form = CompleteForm()
        email = SendEmail()
        form.run()
    finally: 
        if(len(errors) == 0): email.run(f'Tu robot se ha ejecutado sin problemas y ha completado de subir {process[0]} anuncios. !Gracias por confiar en Apartment!')
        else:
            err = 'Ha habido varios errores al intentar ejecutar su robot apartment \n' 
            for i in range (0, len(errors)):
                err = err + f'{i+1}. ' + errors[i] + '\n'
            email.run(err)
            