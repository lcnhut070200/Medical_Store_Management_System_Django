from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics

from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from DjangoMedicalApp.models import Bill, BillDetails, Company, CompanyAccount, CompanyBank, Customer, CustomerRequest, Employee, EmployeeBank, EmployeeSalary, Medicine, MedicalDetails
from DjangoMedicalApp.serializers import  BillDetailsSerializer, BillSerializer, CompanyAccountSerializer, CompanyBankSerializer, CompanySerializer, CustomerRequestSerializer, CustomerSerializer, EmployeeSalarySerializer, MedicineSerializer, MedicalDetailsSerializer, MedicalDetailsSerializerSimple, EmployeeBankSerializer, EmployeeSerializer

from datetime import datetime, timedelta
# Create your views here.

# Company
class CompanyViewSet(viewsets.ViewSet):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def list(self, request):
        company=Company.objects.all()
        serializer=CompanySerializer(company,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Company List Data","data":serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer=CompanySerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Company Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Company Data"}
        return Response(dict_response)


    def retrieve(self,request,pk=None):
        queryset=Company.objects.all()
        company=get_object_or_404(queryset,pk=pk)
        serializer=CompanySerializer(company,context={"request":request})

        serializer_data=serializer.data
        # Adding extra key for medicine details in medicine
        company_bank_details=CompanyBank.objects.filter(company_id=serializer_data["id"])
        company_bank_details_serializer=CompanyBankSerializer(company_bank_details,many=True)
        serializer_data["company_bank"]=company_bank_details_serializer.data

        return Response({"error":False,"message":"Single Data Fetch","data":serializer_data})
        
    def update(self, request,pk=None):
        try:
            queryset=Company.objects.all()
            company=get_object_or_404(queryset,pk=pk)
            serializer=CompanySerializer(company,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Company Data Update Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Updating Company Data"}
        return Response(dict_response)

class CompanyBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        try:
            serializer=CompanyBankSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Company Bank Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Company Bank Data"}
        return Response(dict_response)
    
    def list(self,request):
        companybank=CompanyBank.objects.all()
        serializer=CompanyBankSerializer(companybank,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Company Bank List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=CompanyBank.objects.all()
        companybank=get_object_or_404(queryset,pk=pk)
        serializer=CompanyBankSerializer(companybank,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})
    
    def update(self, request,pk=None):
        try:
            queryset=CompanyBank.objects.all()
            companybank=get_object_or_404(queryset,pk=pk)
            serializer=CompanyBankSerializer(companybank,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"CompanyBank Data Update Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Updating CompanyBank Data"}
        return Response(dict_response)

    def delete(self, request, pk = id):
        try:
            companybank = CompanyBank.objects.filter(id=pk)
            companybank.delete()
            dict_response = {"error": False, "message": "Data Has Been Deleted"}
        except:
            dict_response = {"error": True, "message": "Error During Deleting Company Bank Data"}
        return Response(dict_response)
            
class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer
    def get_queryset(self):
        name=self.kwargs["name"]
        return Company.objects.filter(name=name)

class CompanyOnlyViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer
    def get_queryset(self):
        return Company.objects.all()

class CompanyAccountViewset(viewsets.ViewSet):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def create(self,request):
        try:
            serializer=CompanyAccountSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Company Account Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Company Account Data"}
        return Response(dict_response)

    def list(self,request):
        companyaccount=CompanyAccount.objects.all()
        serializer=CompanyAccountSerializer(companyaccount,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Company Account List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=CompanyAccount.objects.all()
        companyaccount=get_object_or_404(queryset,pk=pk)
        serializer=CompanyAccountSerializer(companyaccount,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=CompanyAccount.objects.all()
        companyaccount=get_object_or_404(queryset,pk=pk)
        serializer=CompanyBankSerializer(companyaccount,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"}) 

# Medicine
class MedicineViewSet(viewsets.ViewSet):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def create(self, request):
        try:
            serializer=MedicineSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            medicine_id=serializer.data['id']
            # Adding and Saving id into medicine details
            medicine_details_list=[]
            for medicine_detail in request.data['medicine_details']:
                medicine_detail["medicine_id"]=medicine_id
                medicine_details_list.append(medicine_detail)
                print(medicine_detail)
                
            serializer2=MedicalDetailsSerializer(data=medicine_details_list,many=True,context={"request":request})
            serializer2.is_valid()
            serializer2.save()

            dict_response={"error":False,"message":"Medicine Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Medicine Data"}
        return Response(dict_response)

    def list(self, request):
        medicine=Medicine.objects.all()
        serializer=MedicineSerializer(medicine,many=True,context={"request":request})

        medicine_data=serializer.data
        newmedicinelist=[]

        # Adding extra key for medicine details in medicine
        for medicine in medicine_data:
            medicine_details=MedicalDetails.objects.filter(medicine_id=medicine["id"])
            medicine_details_serializer=MedicalDetailsSerializerSimple(medicine_details,many=True)
            medicine["medicine_details"]=medicine_details_serializer.data
            newmedicinelist.append(medicine)

        response_dict={"error":False,"message":"All Medicine List Data","data":newmedicinelist}
        return Response(response_dict)
    
    def retrieve(self,request,pk=None):
        queryset=Medicine.objects.all()
        medicine=get_object_or_404(queryset,pk=pk)
        serializer=MedicineSerializer(medicine,context={"request":request})

        serializer_data=serializer.data
        # Adding extra key for medicine details in medicine
        medicine_details=MedicalDetails.objects.filter(medicine_id=serializer_data["id"])
        medicine_details_serializer=MedicalDetailsSerializerSimple(medicine_details,many=True)
        serializer_data["medicine_details"]=medicine_details_serializer.data

        return Response({"error":False,"message":"Single Data Fetch","data":serializer_data})
        
    def update(self, request,pk=None):
        try:
            queryset=Medicine.objects.all()
            medicine=get_object_or_404(queryset,pk=pk)
            serializer=MedicineSerializer(medicine,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            for salt_detail in request.data["medicine_details"]:
                if(salt_detail["id"]==0):
                    # for insert new salt details
                    del salt_detail["id"]
                    salt_detail["medicine_id"]=serializer.data["id"]
                    serializer2=MedicalDetailsSerializer(data=salt_detail,context={"request":request})
                    serializer2.is_valid()
                    serializer2.save()
                else:
                    # for update salt details
                    queryset2=MedicalDetails.objects.all()
                    medicine_salt=get_object_or_404(queryset2,pk=salt_detail["id"])
                    del salt_detail["id"]
                    serializer3=MedicalDetailsSerializer(medicine_salt, data=salt_detail,context={"request":request})
                    serializer3.is_valid()
                    serializer3.save()

            dict_response={"error":False,"message":"Medicine Data Update Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Updating Medicine Data"}
        return Response(dict_response)

    def delete(self, request, pk = id):
        queryset = Medicine.objects.filter()
        medicine = get_object_or_404(queryset, pk = pk)
        medicine.delete()

        return Response({"error": False, "message": "Medicine Data Delete Successfully"})

class MedicineNameViewSet(generics.ListAPIView):
    serializer_class = MedicineSerializer
    def get_queryset(self):
        name=self.kwargs["name"]
        return Medicine.objects.filter(name__contains=name)


# Employee
class EmployeeViewSet(viewsets.ViewSet):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def create(self,request):
        try:
            serializer=EmployeeSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Employee Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Employee Data"}
        return Response(dict_response)

    def list(self,request):
        employee=Employee.objects.all()
        serializer=EmployeeSerializer(employee,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Employee List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=Employee.objects.all()
        employee=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSerializer(employee,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=Employee.objects.all()
        employee=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSerializer(employee,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"}) 

    def delete(self, request, pk = id):
        try:
            employee = Employee.objects.filter(id=pk)
            employee.delete()
            dict_response = {"error": False, "message": "Data Has Been Deleted"}
        except:
            dict_response = {"error": True, "message": "Error During Deleting Company Bank Data"}
        return Response(dict_response)

class EmployeeBankViewSet(viewsets.ViewSet):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self,request):
        try:
            serializer=EmployeeBankSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Employee Bank Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Employee Bank Data"}
        return Response(dict_response)

    def list(self,request):
        employee=EmployeeBank.objects.all()
        serializer=EmployeeBankSerializer(employee,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Employee Bank List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=EmployeeBank.objects.all()
        employeebank=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeBankSerializer(employeebank,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=EmployeeBank.objects.all()
        employeebank=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeBankSerializer(employeebank,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"}) 

class EmployeeSalaryViewSet(viewsets.ViewSet):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self,request):
        try:
            serializer=EmployeeSalarySerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Employee Salary Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Employee Salary Data"}
        return Response(dict_response)

    def list(self,request):
        employeesalary=EmployeeSalary.objects.all()
        serializer=EmployeeSalarySerializer(employeesalary,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Employee Salary List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=EmployeeSalary.objects.all()
        employeesalary=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSalarySerializer(employeesalary,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=EmployeeSalary.objects.all()
        employeesalary=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSalarySerializer(employeesalary,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"}) 

class EmployeeBankByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeBankSerializer
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        employee_id=self.kwargs["employee_id"]
        return EmployeeBank.objects.filter(employee_id=employee_id)

class EmployeeSalaryByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeSalarySerializer
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        employee_id=self.kwargs["employee_id"]
        return EmployeeSalary.objects.filter(employee_id=employee_id)

# Bill
# class GenerateBillViewSet(viewsets.ViewSet): 
#     authentication_classes= [JWTAuthentication]
#     permission_classes=[IsAuthenticated]

#     def create(self, request):
#         # try:
#             # Save customer data
#         serializer = CustomerSerializer(data=request.data, context={"request": request})
#         serializer.is_valid()
#         serializer.save()

#         customer_id=serializer.data['id']

#         # Save bill data
#         billdata={}
#         billdata['customer_id']=customer_id

#         serializer2=BillSerializer(data=billdata,context={"request":request})
#         serializer2.is_valid()
#         serializer2.save()

#         bill_id=serializer.data['id']
#         # Adding and Saving id into medicine details
#         medicine_details_list=[]
#         for medicine_detail in request.data['medicine_details']:
#             medicine_detail1={}
#             medicine_detail1["medicine_id"]=medicine_detail['id']
#             medicine_detail1["bill_id"]= bill_id
#             medicine_detail1["qty"]= medicine_detail['qty']

#             medicine_deduct=Medicine.objects.get(id=medicine_detail["id"])
#             medicine_deduct.in_stock_total=int(medicine_deduct.in_stock_total)-int(medicine_detail['qty'])
#             medicine_deduct.save()

#             medicine_details_list.append(medicine_detail1)
            
#         serializer3=BillDetailsSerializer(data=medicine_details_list,many=True,context={"request":request})
#         serializer3.is_valid()
#         serializer3.save()

#         dict_response={"error":False,"message":"Bill Generata Save Successfully"}
#         # except:
#         #     dict_response={"error":True,"message":"Error During Generating Bill"}
#         return Response(dict_response)

class GenerateBillViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            #Save Customer Data
            serializer = CustomerSerializer(data = request.data, context = {"request": request})
            serializer.is_valid()
            serializer.save()

            customer_id = serializer.data["id"]

            #Save Bill Data
            billData = {}
            billData["customer_id"] = customer_id
            serializer2 = BillSerializer(data = billData, context = {"request": request})
            serializer2.is_valid()
            serializer2.save()

            bill_id = serializer2.data["id"]
            # Access the serializer ID which just save in our db table
            medicine_details_list = []
            for medicine_detail in request.data["medicine_details"]:
                medicine_detail1 = {}
                medicine_detail1["medicine_id"] = medicine_detail["id"]
                medicine_detail1["bill_id"] = bill_id
                medicine_detail1["qty"] = medicine_detail["qty"]

                medicine_deduct = Medicine.objects.get(id=medicine_detail["id"])
                medicine_deduct.in_stock_total = int(medicine_deduct.in_stock_total) - int(medicine_detail["qty"])
                medicine_deduct.save()

                medicine_details_list.append(medicine_detail1)
                # print(medicine_detail)

            serializer3 = BillDetailsSerializer(data = medicine_details_list, many = True, context = {"request": request})
            serializer3.is_valid()
            serializer3.save()

            dict_response = {"error": False, "message": "Bill Generate Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Generating Bill"}
        return Response(dict_response)

# Customer Request
class CustomerRequestViewSet(viewsets.ViewSet):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def list(self, request):
        customer_request=CustomerRequest.objects.all()
        serializer=CustomerRequestSerializer(customer_request,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Customer Request List Data","data":serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer=CustomerRequestSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Customer Request Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Customer Request Data"}
        return Response(dict_response)


    def retrieve(self,request,pk=None):
        queryset=CustomerRequest.objects.all()
        customer_request=get_object_or_404(queryset,pk=pk)
        serializer=CustomerRequestSerializer(customer_request,context={"request":request})

        serializer_data=serializer.data

        return Response({"error":False,"message":"Single Data Fetch","data":serializer_data})
        
    def update(self, request,pk=None):
        try:
            queryset=CustomerRequest.objects.all()
            customer_request=get_object_or_404(queryset,pk=pk)
            serializer=CustomerRequestSerializer(customer_request,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Customer Request Data Update Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Updating Customer Request Data"}
        return Response(dict_response)

# Home viewset
class HomeApiViewSet(viewsets.ViewSet):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def list(self,request):
        customer_request=CustomerRequest.objects.all()
        customer_request_serializer=CustomerRequestSerializer(customer_request,many=True,context={"request":request})

        bill_count=Bill.objects.all()
        bill_count_serializer=BillSerializer(bill_count,many=True,context={"request":request})

        total_medicine=Medicine.objects.all()
        total_medicine_serializer=MedicineSerializer(total_medicine,many=True,context={"request":request})

        total_company=Company.objects.all()
        total_company_serializer=CompanySerializer(total_company,many=True,context={"request":request})

        total_employee=Employee.objects.all()
        total_employee_serializer=EmployeeSerializer(total_employee,many=True,context={"request":request})

        bill_details=BillDetails.objects.all()
        profit_amt=0
        sell_amt=0
        buy_amt=0
        for bill in bill_details:
            buy_amt=float(buy_amt)+float(bill.medicine_id.buy_price)*int(bill.qty)
            sell_amt=float(sell_amt)+float(bill.medicine_id.sell_price)*int(bill.qty)
            
        profit_amt=sell_amt-buy_amt

        customer_request_pending=CustomerRequest.objects.filter(status=False)
        customer_request_pending_serializer=CustomerRequestSerializer(customer_request_pending,many=True,context={"request":request})

        customer_request_completed=CustomerRequest.objects.filter(status=True)
        customer_request_completed_serializer=CustomerRequestSerializer(customer_request_completed,many=True,context={"request":request})

        current_date=datetime.today().strftime("%Y-%m-%d")
        current_date1=datetime.today()
        current_7days=current_date1+timedelta(days=7)
        current_7days=current_7days.strftime("%Y-%m-%d")

        bill_details_today=BillDetails.objects.filter(added_on__date=current_date)
        profit_amt_today=0
        sell_amt_today=0
        buy_amt_today=0
        for bill in bill_details_today:
            buy_amt_today=float(buy_amt_today)+float(bill.medicine_id.buy_price)*int(bill.qty)
            sell_amt_today=float(sell_amt_today)+float(bill.medicine_id.sell_price)*int(bill.qty)

        profit_amt_today=sell_amt_today-buy_amt_today

        medicine_expire_in_week=Medicine.objects.filter(expire_date__range=[current_date,current_7days])
        medicine_expire_in_week_serializer=MedicineSerializer(medicine_expire_in_week,many=True,context={"request":request})


        bill_dates=BillDetails.objects.order_by().values("added_on__date").distinct()
        profit_chart_list=[]
        sell_chart_list=[]
        buy_chart_list=[]

        for billdate in bill_dates:
            access_date=billdate["added_on__date"]
            
            bill_data=BillDetails.objects.filter(added_on__date=access_date)
            profit_amt_inner=0
            sell_amt_inner=0
            buy_amt_inner=0

            for billsingle in bill_data:
                buy_amt_inner=float(buy_amt_inner)+float(billsingle.medicine_id.buy_price)*int(billsingle.qty)
                sell_amt_inner=float(sell_amt_inner)+float(billsingle.medicine_id.sell_price)*int(billsingle.qty)

            profit_amt_inner=sell_amt_inner-buy_amt_inner
            profit_chart_list.append({"date":access_date,"amt":profit_amt_inner})
            sell_chart_list.append({"date":access_date,"amt":sell_amt_inner})
            buy_chart_list.append({"date":access_date,"amt":buy_amt_inner})


        dict_response={"error":False,"message":"Home Page Data","customer_request":len(customer_request_serializer.data), "bill_count":len(bill_count_serializer.data), "total_medicine":len(total_medicine_serializer.data), "total_company":len(total_company_serializer.data),"total_employee":len(total_employee_serializer.data),"total_sell":sell_amt,"total_buy":buy_amt, "total_profit":profit_amt,"customer_request_pending":len(customer_request_pending_serializer.data),"customer_request_completed":len(customer_request_completed_serializer.data),"total_profit_today":profit_amt_today,"total_sell_today":sell_amt_today,"medicine_expire_in_week":len(medicine_expire_in_week_serializer.data),"sell_chart":sell_chart_list,"buy_chart":buy_chart_list,"profit_chart":profit_chart_list}
        return Response(dict_response)

company_list=CompanyViewSet.as_view({"get":"list"})
company_create=CompanyViewSet.as_view({"post":"create"})
company_update=CompanyViewSet.as_view({"put":"update"})
