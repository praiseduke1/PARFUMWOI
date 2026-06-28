import logging

from django.core.validators import MinValueValidator
from django.db import models
from django.core.cache import cache

logger = logging.getLogger(__name__)


class ShippingConfig(models.Model):
    origin_province = models.CharField('Provinsi Asal', max_length=100, default='Jawa Tengah')
    origin_city = models.CharField('Kota/Kabupaten Asal', max_length=100, default='Kabupaten Banyumas')
    origin_district = models.CharField('Kecamatan Asal', max_length=100, default='Purwokerto')
    origin_district_code = models.CharField('Kode Kecamatan Asal', max_length=10, default='', blank=True)
    komerce_origin_id = models.PositiveIntegerField('ID Origin Komerce', null=True, blank=True)
    default_weight = models.PositiveIntegerField('Berat Default (gram)', default=500)
    cache_ttl = models.PositiveIntegerField('Cache TTL (menit)', default=10)
    enabled_couriers = models.TextField(
        'Kurir Aktif',
        default='jne,jnt,sicepat,pos,anteraja,ninja,tiki,lion,sap,idexpress',
    )

    class Meta:
        verbose_name = 'Konfigurasi Pengiriman'
        verbose_name_plural = 'Konfigurasi Pengiriman'

    def __str__(self):
        return f'{self.origin_district}, {self.origin_city}'

    def get_enabled_couriers(self):
        return [c.strip() for c in self.enabled_couriers.split(',') if c.strip()]

    @classmethod
    def get_config(cls):
        key = 'shipping:config'
        config = cache.get(key)
        if config is None:
            config = cls.load()
            cache.set(key, config, 300)
        return config

    @classmethod
    def load(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
            logger.info('Created default ShippingConfig')
        return obj

    @classmethod
    def clear_cache(cls):
        cache.delete('shipping:config')


class Courier(models.Model):
    code = models.CharField('Kode Kurir', max_length=20, unique=True)
    name = models.CharField('Nama Kurir', max_length=100)
    logo_url = models.URLField('URL Logo', blank=True)

    COURIER_COLORS = {
        'jne': '#0054A0',
        'jnt': '#E31E24',
        'sicepat': '#00A650',
        'pos': '#F58220',
        'anteraja': '#6A0DAD',
        'ninja': '#FF6600',
        'tiki': '#0033A0',
        'lion': '#FFD700',
        'sap': '#008000',
        'idexpress': '#1E90FF',
    }

    class Meta:
        verbose_name = 'Kurir'
        verbose_name_plural = 'Kurir'
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def get_default_couriers(cls):
        prefix = '/static/images/couriers/'
        return {
            'jne': {'name': 'JNE', 'logo': f'{prefix}jne.svg'},
            'jnt': {'name': 'J&T', 'logo': f'{prefix}jnt.svg'},
            'sicepat': {'name': 'SiCepat', 'logo': f'{prefix}sicepat.svg'},
            'pos': {'name': 'POS Indonesia', 'logo': f'{prefix}pos.svg'},
            'anteraja': {'name': 'AnterAja', 'logo': f'{prefix}anteraja.svg'},
            'ninja': {'name': 'Ninja Xpress', 'logo': f'{prefix}ninja.svg'},
            'tiki': {'name': 'TIKI', 'logo': f'{prefix}tiki.svg'},
            'lion': {'name': 'Lion Parcel', 'logo': f'{prefix}lion.svg'},
            'sap': {'name': 'SAP Express', 'logo': ''},
            'idexpress': {'name': 'ID Express', 'logo': f'{prefix}idexpress.svg'},
        }
