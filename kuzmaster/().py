# coding: utf-8
a = Avans.objects.all()
a
a.amount
a[0].amount
a.pop(0)
del a
get_ipython().run_line_magic('save', '()')
a = Avans.objects.all()
a
a.clear()
a.delete()
a.save()
