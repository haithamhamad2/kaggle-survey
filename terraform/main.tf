terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

resource "google_compute_address" "default" {
  name   = "my-static-ip-address"
  region = var.region
}

resource "google_compute_instance" "kagglesv1722" {
  boot_disk {
    auto_delete = true
    device_name = "kagglesv1722"

    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20240307b"
      size  = 10
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  labels = {
    goog-ec-src = "vm_add-tf"
  }

  machine_type = "e2-standard-2"
  name         = "kagglesv1722"

  network_interface {
    access_config {
      network_tier = "PREMIUM"
      nat_ip = google_compute_address.default.address
    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = "projects/kaggle-ml-ds-survey/regions/us-west4/subnetworks/default"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = "491007980607-compute@developer.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/devstorage.read_only", "https://www.googleapis.com/auth/logging.write", "https://www.googleapis.com/auth/monitoring.write", "https://www.googleapis.com/auth/service.management.readonly", "https://www.googleapis.com/auth/servicecontrol", "https://www.googleapis.com/auth/trace.append"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  tags = ["http-server", "https-server"]
  zone = var.zone
}

resource "google_compute_firewall" "rules" {
  project     = var.project
  name        = "myfirewallrule"
  network     = "default"
  description = "Creates firewall rule targeting tagged instances"

  allow {
    protocol  = "tcp"
    ports     = ["4040", "6789", "7077", "8080-8082", "8888-8898"]
  }
  source_ranges = ["0.0.0.0/0"]
}

resource "google_storage_bucket" "kaggle_ml_ds_survey_bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "kaggle_ml_ds_survey_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}