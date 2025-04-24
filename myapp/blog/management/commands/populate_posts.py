from blog.models import Post, Category
from django.core.management.base import BaseCommand
import random



class Command(BaseCommand):
    help = "This commands inserts post data"

    def handle(self, *args, **options):

        # Delete existing data
        Post.objects.all().delete()

        titles = [
            "Clement of Rome",
            "Ignatius of Antioch",
            "Polycarp",
            "Papias of Hierapolis",
            "Augustine of Hippo",
            "Ambrose of Milan",
            "Jerome",
            "Pope Gregory I",
            "Athanasius of Alexandria",
            "Basil of Caesarea",
            "Gregory of Nazianzus",
            "Gregory of Nyssa",
            "John Chrysostom",
            "Cyril of Alexandria",
            "Tertullian",
            "Origen of Alexandria",
            "Irenaeus of Lyon",
            "Cyprian of Carthage",
            "Leo the Great",
            "John of Damascus"
        ]

        contents = [
            "Bishop of Rome, known for his letters to the church at Corinth, offering guidance and theological insights",
            "Bishop of Antioch, famous for his letters written during his journey to Rome for execution, emphasizing the importance of unity and obedience to the church leadership",
            "Bishop of Smyrna, a disciple of the apostle John and a martyr, known for his defense of the Christian faith and emphasis on ethical living",
            "Bishop of Hierapolis, known for his work on the sayings of Jesus and his understanding of the early Christian church",
            "Bishop of Hippo, one of the most influential figures in Western Christianity, his works, shaped theological doctrines on grace, free will, and the nature of God",
            "Bishop of Milan, a powerful figure who defended the church against heresy and contributed to the development of church music and liturgy",
            "A scholar and translator of the Bible, he produced the Latin Vulgate translation, which became the standard Bible for the Western Church for centuries",
            "Pope of Rome, also known as Gregory the Great, his writings on pastoral care, theology, and church governance were influential",
            "Patriarch of Alexandria, defender of Nicene Christianity against Arianism, known for his work 'On the Incarnation' and his role in the Council of Nicaea",
            "Bishop of Caesarea, one of the Cappadocian Fathers, known for his monastic rule and his contributions to Trinitarian theology",
            "Archbishop of Constantinople, one of the Cappadocian Fathers, known as 'The Theologian' for his orations and poetry on the Trinity",
            "Bishop of Nyssa, one of the Cappadocian Fathers, known for his mystical theology and contributions to the doctrine of the Trinity",
            "Archbishop of Constantinople, renowned for his eloquent preaching (hence 'Chrysostom' or 'golden-mouthed') and biblical commentaries",
            "Patriarch of Alexandria, known for his defense of the title 'Theotokos' for Mary and his role in the Council of Ephesus",
            "North African theologian, known for his extensive writings on Christian doctrine and practice, though later associated with Montanism",
            "Alexandrian theologian and biblical scholar, known for his allegorical interpretation of Scripture and his controversial speculative theology",
            "Bishop of Lyon, known for his work 'Against Heresies' which refuted Gnosticism and emphasized apostolic succession",
            "Bishop of Carthage, known for his emphasis on church unity and his writings during the Novatian schism and Decian persecution",
            "Pope of Rome, known for his encounter with Attila the Hun, his theological work 'Tome of Leo,' and his influence on the Council of Chalcedon",
            "Syrian monk and priest, known as the last of the Greek Fathers, famous for his defense of icons and his work 'The Fount of Knowledge'"
        ]

        img_urls = [
            "https://picsum.photos/id/1/800/400",
            "https://picsum.photos/id/2/800/400",
            "https://picsum.photos/id/3/800/400",
            "https://picsum.photos/id/4/800/400",
            "https://picsum.photos/id/5/800/400",
            "https://picsum.photos/id/6/800/400",
            "https://picsum.photos/id/7/800/400",
            "https://picsum.photos/id/8/800/400",
            "https://picsum.photos/id/9/800/400",
            "https://picsum.photos/id/10/800/400",
            "https://picsum.photos/id/11/800/400",
            "https://picsum.photos/id/12/800/400",
            "https://picsum.photos/id/13/800/400",
            "https://picsum.photos/id/14/800/400",
            "https://picsum.photos/id/15/800/400",
            "https://picsum.photos/id/16/800/400",
            "https://picsum.photos/id/17/800/400",
            "https://picsum.photos/id/18/800/400",
            "https://picsum.photos/id/19/800/400",
            "https://picsum.photos/id/20/800/400"
        ]

        categories = Category.objects.all()
        for title, content, img_url in zip(titles,contents,img_urls):
            category = random.choice(categories)
            Post.objects.create(title=title, content=content, img_url=img_url,category=category)
        self.stdout.write(self.style.SUCCESS("Completed Inserting Data!"))


