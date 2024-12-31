<template>
    <div class="container d-flex justify-content-center align-items-center mt-5">
      <div class="col-md-8 d-inline-block p-4 bg-white bg-opacity-75 rounded shadow">
        <div class="card p-4 bg-white bg-opacity-75">
          <h1 class="card-title">Make Payment</h1>
          
          <form @submit.prevent="makePayment">
            <div class="form-group p-2">
              <label for="influencer_name" class="card-text">Influencer Name</label>
              <input type="text" v-model="adRequest.influencer_name" class="form-control" readonly>
            </div>
            
            <div class="form-group p-2">
              <label for="sponsor_name" class="card-text">Sponsor Name</label>
              <input type="text" v-model="adRequest.sponsor_name" class="form-control" readonly>
            </div>
            
            <div class="form-group p-2">
              <label for="campaign_name" class="card-text">Campaign Name</label>
              <input type="text" v-model="adRequest.campaign_name" class="form-control" readonly>
            </div>
            
            <div class="form-group p-2">
              <label for="payment_amount" class="card-text">Payment Amount</label>
              <input type="number" v-model="adRequest.payment_amount" class="form-control">
            </div>
  
            <div class="form-group mt-3 p-2">
              <button type="submit" class="btn btn-success" :disabled="isPaymentInProgress">
                <i class="fa-solid fa-money-bill"></i> Make Payment
              </button>
              <!-- Show view invoice button if payment has been made -->
              <button v-if="adRequest.payment_status === true" @click="viewInvoice" class="btn btn-info ml-2">
                <i class="fa-solid fa-file-invoice"></i> View Invoice
              </button>
            </div>
          </form>

          <!-- Invoice Details Modal -->
          
          <!-- Invoice Details Modal -->
        <div v-if="showInvoiceModal" class="invoice-modal">
          <div class="invoice-modal-content">
            <div class="invoice-modal-header">
              <h2>AdConnect Invoice</h2>
              <button @click="closeInvoiceModal" class="close-btn">&times;</button>
            </div>
            <div class="invoice-modal-body">
              <div class="invoice-header">
                <div class="logo-section">
                  <h1>AdConnect</h1>
                  <p>Connecting Brands and Influencers</p>
                </div>
                <div class="invoice-details-header">
                  <div class="invoice-number">
                    <strong>Invoice #</strong>
                    <span>{{ invoiceDetails.id }}</span>
                  </div>
                  <div class="invoice-date">
                    <strong>Date</strong>
                    <span>{{ getCurrentDate() }}</span>
                  </div>
                </div>
              </div>

              <div class="invoice-body">
                <div class="invoice-section">
                  <h3>Transaction Details</h3>
                  <table>
                    <thead>
                        <tr>
                          <th>Campaign Name</th>
                          <td>{{ invoiceDetails.campaign_name }}</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                          <th>Sponsor Name</th>
                          <td>{{ invoiceDetails.sponsor_name }}</td>
                        </tr>
                        <tr>
                          <th>Influencer Name</th>
                          <td>{{ invoiceDetails.influencer_name }}</td>
                        </tr>
                    </tbody>
                  </table>
                </div>

                <div class="invoice-section payment-section">
                  <h3>Payment Information</h3>
                  <table>
                <thead>
                    <tr>
                    <th>Payment Details</th>
                    <th>Information</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <th>Payment Amount</th>
                    <td>₹{{ formatCurrency(invoiceDetails.payment_amount) }}</td>
                    </tr>
                    <tr>
                    <th>Payment Status</th>
                    <td>
                        <span :class="invoiceDetails.payment_status ? 'status-paid' : 'status-pending'">
                        {{ invoiceDetails.payment_status ? 'Paid' : 'Pending' }}
                        </span>
                    </td>
                    </tr>
                </tbody>
                </table>
                </div>
              </div>

              <div class="invoice-footer">
                <p>Thank you for your business!</p>
                <p>© 2024 AdConnect. All rights reserved.</p>
              </div>
            </div>
          </div>
        </div>
          





        </div>
      </div>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
  data() {
    return {
      adRequest: {
        influencer_name: '',
        sponsor_name: '',
        campaign_name: '',
        payment_amount: '',
        payment_status: false,
      },
      isPaymentInProgress: false,
      showInvoiceModal: false,
      invoiceDetails: null
    };
  },
  created() {
    this.fetchAdRequestData();
  },
  methods: {
    fetchAdRequestData() {
      const accessToken = localStorage.getItem('token');
      const adRequestId = this.$route.params.id;
      axios.get(`/sponsor/ad_requests/${adRequestId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then(response => {
        this.adRequest = response.data;
      })
      .catch(error => {
        console.error('Error fetching ad request data:', error);
      });
    },
    makePayment() {
      const accessToken = localStorage.getItem('token');
      const adRequestId = this.$route.params.id;
      const data = {
        payment_amount: this.adRequest.payment_amount,
      };

      this.isPaymentInProgress = true;

      axios.post(`/sponsor/make_payment/${adRequestId}`, data, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        }
      })
      .then(() => {
        this.adRequest.payment_status = true; 
        this.isPaymentInProgress = false; 
      })
      .catch(error => {
        console.error('Error processing payment:', error);
        this.isPaymentInProgress = false;
      });
    },
    viewInvoice() {
    //   const accessToken = localStorage.getItem('token');
      const adRequestId = this.$route.params.id;

      // Use the existing ad request data to populate invoice details
      this.invoiceDetails = {
        id: adRequestId,
        campaign_name: this.adRequest.campaign_name,
        sponsor_name: this.adRequest.sponsor_name,
        influencer_name: this.adRequest.influencer_name,
        payment_amount: this.adRequest.payment_amount,
        payment_status: this.adRequest.payment_status
      };

      this.showInvoiceModal = true;
    },
    closeInvoiceModal() {
      this.showInvoiceModal = false;
      this.invoiceDetails = null;
    },
    getCurrentDate() {
      return new Date().toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      });
    },
    formatCurrency(amount) {
      return parseFloat(amount).toFixed(2);
    }
  },
};
</script>


<style scoped>
/* Invoice Modal Styles */
.invoice-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.invoice-modal-content {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.invoice-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #f4f4f4;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.invoice-modal-header h2 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #888;
  cursor: pointer;
}

.invoice-modal-body {
  padding: 20px;
}

.invoice-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.logo-section h1 {
  color: #2c3e50;
  margin: 0;
  font-size: 2rem;
}

.logo-section p {
  color: #7f8c8d;
  margin: 5px 0 0;
}

.invoice-details-header {
  text-align: right;
}

.invoice-details-header div {
  margin-bottom: 10px;
}

.invoice-body {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.invoice-section {
  width: 48%;
}

.invoice-section h3 {
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
  color: #2c3e50;
  margin-bottom: 15px;
}

.invoice-section table {
  width: 100%;
  border-collapse: collapse;
}

.invoice-section table th,
.invoice-section table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ecf0f1;
}

.invoice-section table th {
  color: #2c3e50;
  font-weight: 600;
}

.payment-section .status-paid {
  color: #2ecc71;
  font-weight: bold;
}

.payment-section .status-pending {
  color: #f39c12;
  font-weight: bold;
}

.invoice-footer {
  text-align: center;
  padding: 20px;
  background-color: #f4f4f4;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}

.invoice-footer p {
  margin: 5px 0;
  color: #7f8c8d;
}
</style>
