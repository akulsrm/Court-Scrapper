// Court data
const HIGH_COURTS = {
    "Allahabad": "1",
    "Bombay": "2",
    "Delhi": "3",
    "Madras": "4",
    "Karnataka": "5",
    "Madhya Pradesh": "6"
};

const DISTRICT_COURTS = {
    "Delhi": "1",
    "Mumbai": "2",
    "Chennai": "3",
    "Bangalore": "4"
};

// Populate court names based on court type selection
function populateCourtNames(courtTypeId, courtNameId) {
    const courtType = $(`#${courtTypeId}`).val();
    const courtNameSelect = $(`#${courtNameId}`);
    
    // Clear previous options
    courtNameSelect.empty();
    courtNameSelect.append('<option value="">Select Court Name</option>');
    
    // Add court options based on type
    if (courtType === 'high') {
        Object.keys(HIGH_COURTS).forEach(court => {
            courtNameSelect.append(`<option value="${court}">${court}</option>`);
        });
    } else if (courtType === 'district') {
        Object.keys(DISTRICT_COURTS).forEach(court => {
            courtNameSelect.append(`<option value="${court}">${court}</option>`);
        });
    }
}

// Format date for display
function formatDate(dateString) {
    if (!dateString) return 'Not Available';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    });
}

// Handle case search form submission
$('#caseSearchForm').on('submit', function(e) {
    e.preventDefault();
    
    // Show loader
    $('#loader').show();
    
    // Hide previous results
    $('.result-section').hide();
    
    // Get form data
    const data = {
        court_type: $('#courtType').val(),
        court_name: $('#courtName').val(),
        case_type: $('#caseType').val(),
        case_number: $('#caseNumber').val(),
        year: $('#caseYear').val()
    };
    
    // Send API request
    $.ajax({
        url: '/api/search',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            // Hide loader
            $('#loader').hide();
            
            // Display case details
            $('#resultCourt').text(response.court);
            $('#resultCaseType').text(response.case_type);
            $('#resultCaseNumber').text(response.case_number);
            $('#resultYear').text(response.year);
            $('#resultStatus').text(response.status);
            
            $('#resultPetitioner').text(response.parties.petitioner);
            $('#resultRespondent').text(response.parties.respondent);
            $('#resultFilingDate').text(formatDate(response.filing_date));
            $('#resultNextHearing').text(formatDate(response.next_hearing_date));
            
            // Display documents
            const documentsContainer = $('#documentsContainer');
            documentsContainer.empty();
            
            if (response.documents && response.documents.length > 0) {
                response.documents.forEach(doc => {
                    if (doc.id) {
                        const docDate = doc.date ? formatDate(doc.date) : 'N/A';
                        const docItem = `
                            <div class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <h6>${doc.type.charAt(0).toUpperCase() + doc.type.slice(1)}</h6>
                                    <small>Date: ${docDate}</small>
                                </div>
                                <button class="btn btn-sm btn-primary download-btn" 
                                        data-case-id="${response.case_id}" 
                                        data-doc-type="${doc.type}">
                                    Download
                                </button>
                            </div>
                        `;
                        documentsContainer.append(docItem);
                    }
                });
            } else {
                documentsContainer.append('<div class="list-group-item">No documents available</div>');
            }
            
            // Show results section
            $('#caseResultSection').show();
            $('#caseError').hide();
        },
        error: function(xhr) {
            // Hide loader
            $('#loader').hide();
            
            // Show error message
            let errorMsg = 'An error occurred while fetching case details.';
            if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMsg = xhr.responseJSON.error;
            }
            
            $('#caseError').text(errorMsg).show();
            $('#caseResultSection').show();
            $('#caseDetails').hide();
        }
    });
});

// Handle cause list form submission
$('#causeListForm').on('submit', function(e) {
    e.preventDefault();
    
    // Show loader
    $('#loader').show();
    
    // Hide previous results
    $('.result-section').hide();
    
    // Get form data
    const data = {
        court_type: $('#clCourtType').val(),
        court_name: $('#clCourtName').val(),
        date: $('#clDate').val()
    };
    
    // Send API request
    $.ajax({
        url: '/api/causelist',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            // Hide loader
            $('#loader').hide();
            
            // Display cause list details
            $('#clResultCourt').text(response.court);
            $('#clResultDate').text(formatDate(response.date));
            
            // Display cause list table
            const causeListTable = $('#causeListTable');
            causeListTable.empty();
            
            if (response.cases && response.cases.length > 0) {
                response.cases.forEach(item => {
                    const row = `
                        <tr>
                            <td>${item.serial_no}</td>
                            <td>${item.case_type}</td>
                            <td>${item.case_number}</td>
                            <td>${item.year}</td>
                            <td>${item.parties}</td>
                            <td>${item.purpose}</td>
                        </tr>
                    `;
                    causeListTable.append(row);
                });
            } else {
                causeListTable.append('<tr><td colspan="6" class="text-center">No cases found</td></tr>');
            }
            
            // Show results section
            $('#causeListResultSection').show();
            $('#causeListError').hide();
        },
        error: function(xhr) {
            // Hide loader
            $('#loader').hide();
            
            // Show error message
            let errorMsg = 'An error occurred while fetching cause list.';
            if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMsg = xhr.responseJSON.error;
            }
            
            $('#causeListError').text(errorMsg).show();
            $('#causeListResultSection').show();
            $('#causeListDetails').hide();
        }
    });
});

// Handle document download
$(document).on('click', '.download-btn', function() {
    const caseId = $(this).data('case-id');
    const docType = $(this).data('doc-type');
    
    // Send download request
    $.ajax({
        url: '/api/download',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            case_id: caseId,
            document_type: docType
        }),
        success: function(response) {
            if (response.file_path) {
                // Create download link
                window.location.href = `/downloads/${response.file_path}`;
            } else {
                alert('Failed to download document.');
            }
        },
        error: function() {
            alert('An error occurred while downloading the document.');
        }
    });
});

// Initialize court type change handlers
$('#courtType').on('change', function() {
    populateCourtNames('courtType', 'courtName');
});

$('#clCourtType').on('change', function() {
    populateCourtNames('clCourtType', 'clCourtName');
});

// Initialize date field with current date
$(document).ready(function() {
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    $('#clDate').val(formattedDate);
});